"""
Sistema de Encriptación de Datos - Copilot Salud Andalucía
Encriptación segura de datos sensibles y gestión de claves
"""

import os
import base64
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Dict, Any, Optional, Union
import streamlit as st

class DataEncryption:
    def __init__(self):
        """Inicializar sistema de encriptación"""
        self.key_file = "data/.encryption_key"
        self.salt_file = "data/.encryption_salt"
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
        
        # Configuración de encriptación
        self.encryption_config = {
            'algorithm': 'Fernet',
            'key_derivation': 'PBKDF2HMAC',
            'iterations': 100000,
            'salt_length': 32
        }
    
    def _get_or_create_key(self) -> bytes:
        """Obtener o crear clave de encriptación"""
        try:
            if os.path.exists(self.key_file):
                with open(self.key_file, "rb") as f:
                    return f.read()
            else:
                # Crear nueva clave
                key = Fernet.generate_key()
                self._save_key_securely(key)
                return key
        except Exception as e:
            st.error(f"❌ Error gestionando clave de encriptación: {str(e)}")
            # Generar clave temporal (no persistente)
            return Fernet.generate_key()
    
    def _save_key_securely(self, key: bytes) -> None:
        """Guardar clave de forma segura"""
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(self.key_file), exist_ok=True)
            
            # Guardar clave
            with open(self.key_file, "wb") as f:
                f.write(key)
            
            # Establecer permisos restrictivos (solo propietario puede leer)
            os.chmod(self.key_file, 0o600)
            
        except Exception as e:
            st.error(f"❌ Error guardando clave: {str(e)}")
    
    def _get_or_create_salt(self) -> bytes:
        """Obtener o crear salt para derivación de claves"""
        try:
            if os.path.exists(self.salt_file):
                with open(self.salt_file, "rb") as f:
                    return f.read()
            else:
                # Crear nuevo salt
                salt = os.urandom(32)
                self._save_salt_securely(salt)
                return salt
        except Exception as e:
            st.error(f"❌ Error gestionando salt: {str(e)}")
            return os.urandom(32)
    
    def _save_salt_securely(self, salt: bytes) -> None:
        """Guardar salt de forma segura"""
        try:
            os.makedirs(os.path.dirname(self.salt_file), exist_ok=True)
            
            with open(self.salt_file, "wb") as f:
                f.write(salt)
            
            os.chmod(self.salt_file, 0o600)
            
        except Exception as e:
            st.error(f"❌ Error guardando salt: {str(e)}")
    
    def encrypt_sensitive_data(self, data: Union[Dict, str, bytes]) -> str:
        """Encriptar datos sensibles"""
        try:
            # Convertir datos a JSON si es necesario
            if isinstance(data, (dict, list)):
                json_data = json.dumps(data, ensure_ascii=False)
            elif isinstance(data, str):
                json_data = data
            elif isinstance(data, bytes):
                json_data = data.decode('utf-8')
            else:
                json_data = str(data)
            
            # Encriptar
            encrypted_data = self.cipher.encrypt(json_data.encode('utf-8'))
            
            # Codificar en base64 para almacenamiento
            return base64.b64encode(encrypted_data).decode('utf-8')
            
        except Exception as e:
            st.error(f"❌ Error encriptando datos: {str(e)}")
            raise ValueError(f"Error encriptando datos: {str(e)}")
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> Union[Dict, str]:
        """Desencriptar datos sensibles"""
        try:
            # Decodificar desde base64
            encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            
            # Desencriptar
            decrypted_data = self.cipher.decrypt(encrypted_bytes)
            
            # Intentar parsear como JSON
            try:
                return json.loads(decrypted_data.decode('utf-8'))
            except json.JSONDecodeError:
                # Si no es JSON válido, devolver como string
                return decrypted_data.decode('utf-8')
                
        except Exception as e:
            st.error(f"❌ Error desencriptando datos: {str(e)}")
            raise ValueError(f"Error desencriptando datos: {str(e)}")
    
    def encrypt_user_credentials(self, username: str, password: str, 
                               additional_data: Dict = None) -> str:
        """Encriptar credenciales de usuario de forma segura"""
        try:
            credentials = {
                'username': username,
                'password': password,
                'encrypted_at': self._get_timestamp(),
                'additional_data': additional_data or {}
            }
            
            return self.encrypt_sensitive_data(credentials)
            
        except Exception as e:
            st.error(f"❌ Error encriptando credenciales: {str(e)}")
            raise
    
    def decrypt_user_credentials(self, encrypted_credentials: str) -> Dict:
        """Desencriptar credenciales de usuario"""
        try:
            return self.decrypt_sensitive_data(encrypted_credentials)
        except Exception as e:
            st.error(f"❌ Error desencriptando credenciales: {str(e)}")
            raise
    
    def encrypt_personal_data(self, personal_data: Dict) -> str:
        """Encriptar datos personales sensibles"""
        try:
            # Validar que contiene datos sensibles
            sensitive_fields = ['email', 'phone', 'address', 'dni', 'medical_data']
            has_sensitive = any(field in personal_data for field in sensitive_fields)
            
            if not has_sensitive:
                st.warning("⚠️ No se detectaron campos sensibles en los datos")
            
            # Añadir metadatos de encriptación
            encrypted_package = {
                'data': personal_data,
                'encrypted_at': self._get_timestamp(),
                'sensitive_fields': [field for field in sensitive_fields if field in personal_data],
                'encryption_version': '1.0'
            }
            
            return self.encrypt_sensitive_data(encrypted_package)
            
        except Exception as e:
            st.error(f"❌ Error encriptando datos personales: {str(e)}")
            raise
    
    def decrypt_personal_data(self, encrypted_personal_data: str) -> Dict:
        """Desencriptar datos personales"""
        try:
            return self.decrypt_sensitive_data(encrypted_personal_data)
        except Exception as e:
            st.error(f"❌ Error desencriptando datos personales: {str(e)}")
            raise
    
    def encrypt_audit_log(self, audit_entry: Dict) -> str:
        """Encriptar entrada de log de auditoría"""
        try:
            # Añadir metadatos de seguridad
            secure_entry = {
                'entry': audit_entry,
                'encrypted_at': self._get_timestamp(),
                'integrity_hash': self._calculate_integrity_hash(audit_entry)
            }
            
            return self.encrypt_sensitive_data(secure_entry)
            
        except Exception as e:
            st.error(f"❌ Error encriptando log de auditoría: {str(e)}")
            raise
    
    def decrypt_audit_log(self, encrypted_audit_log: str) -> Dict:
        """Desencriptar log de auditoría"""
        try:
            decrypted_data = self.decrypt_sensitive_data(encrypted_audit_log)
            
            # Verificar integridad
            if 'integrity_hash' in decrypted_data:
                expected_hash = decrypted_data['integrity_hash']
                actual_hash = self._calculate_integrity_hash(decrypted_data['entry'])
                
                if expected_hash != actual_hash:
                    st.warning("⚠️ Posible manipulación detectada en log de auditoría")
            
            return decrypted_data
            
        except Exception as e:
            st.error(f"❌ Error desencriptando log de auditoría: {str(e)}")
            raise
    
    def encrypt_file(self, file_path: str, output_path: str = None) -> str:
        """Encriptar archivo completo"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
            
            # Leer archivo
            with open(file_path, "rb") as f:
                file_data = f.read()
            
            # Encriptar
            encrypted_data = self.cipher.encrypt(file_data)
            
            # Determinar ruta de salida
            if output_path is None:
                output_path = file_path + ".encrypted"
            
            # Guardar archivo encriptado
            with open(output_path, "wb") as f:
                f.write(encrypted_data)
            
            # Establecer permisos restrictivos
            os.chmod(output_path, 0o600)
            
            return output_path
            
        except Exception as e:
            st.error(f"❌ Error encriptando archivo: {str(e)}")
            raise
    
    def decrypt_file(self, encrypted_file_path: str, output_path: str = None) -> str:
        """Desencriptar archivo"""
        try:
            if not os.path.exists(encrypted_file_path):
                raise FileNotFoundError(f"Archivo encriptado no encontrado: {encrypted_file_path}")
            
            # Leer archivo encriptado
            with open(encrypted_file_path, "rb") as f:
                encrypted_data = f.read()
            
            # Desencriptar
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            # Determinar ruta de salida
            if output_path is None:
                if encrypted_file_path.endswith(".encrypted"):
                    output_path = encrypted_file_path[:-10]  # Quitar .encrypted
                else:
                    output_path = encrypted_file_path + ".decrypted"
            
            # Guardar archivo desencriptado
            with open(output_path, "wb") as f:
                f.write(decrypted_data)
            
            return output_path
            
        except Exception as e:
            st.error(f"❌ Error desencriptando archivo: {str(e)}")
            raise
    
    def _calculate_integrity_hash(self, data: Dict) -> str:
        """Calcular hash de integridad para verificar datos"""
        import hashlib
        
        # Convertir datos a string consistente
        data_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
        
        # Calcular hash SHA-256
        return hashlib.sha256(data_str.encode('utf-8')).hexdigest()
    
    def _get_timestamp(self) -> str:
        """Obtener timestamp actual"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def rotate_encryption_key(self, new_password: str = None) -> bool:
        """Rotar clave de encriptación (requiere re-encriptar todos los datos)"""
        try:
            # Generar nueva clave
            new_key = Fernet.generate_key()
            
            # Guardar clave anterior para migración
            old_key = self.key
            old_cipher = Fernet(old_key)
            
            # Actualizar clave actual
            self.key = new_key
            self.cipher = Fernet(new_key)
            
            # Guardar nueva clave
            self._save_key_securely(new_key)
            
            st.success("✅ Clave de encriptación rotada exitosamente")
            st.warning("⚠️ Nota: Los datos existentes necesitarán ser re-encriptados con la nueva clave")
            
            return True
            
        except Exception as e:
            st.error(f"❌ Error rotando clave de encriptación: {str(e)}")
            # Restaurar clave anterior
            self.key = old_key
            self.cipher = old_cipher
            return False
    
    def get_encryption_status(self) -> Dict[str, Any]:
        """Obtener estado del sistema de encriptación"""
        try:
            status = {
                'algorithm': self.encryption_config['algorithm'],
                'key_derivation': self.encryption_config['key_derivation'],
                'key_exists': os.path.exists(self.key_file),
                'salt_exists': os.path.exists(self.salt_file),
                'key_file_permissions': self._get_file_permissions(self.key_file),
                'salt_file_permissions': self._get_file_permissions(self.salt_file),
                'last_modified': self._get_file_modified_time(self.key_file)
            }
            
            return status
            
        except Exception as e:
            return {'error': str(e)}
    
    def _get_file_permissions(self, file_path: str) -> str:
        """Obtener permisos del archivo en formato octal"""
        try:
            if os.path.exists(file_path):
                stat_info = os.stat(file_path)
                return oct(stat_info.st_mode)[-3:]
            return "N/A"
        except:
            return "N/A"
    
    def _get_file_modified_time(self, file_path: str) -> str:
        """Obtener tiempo de modificación del archivo"""
        try:
            if os.path.exists(file_path):
                import datetime
                mtime = os.path.getmtime(file_path)
                return datetime.datetime.fromtimestamp(mtime).isoformat()
            return "N/A"
        except:
            return "N/A"
    
    def validate_encryption_integrity(self) -> Dict[str, Any]:
        """Validar integridad del sistema de encriptación"""
        try:
            # Test de encriptación/desencriptación
            test_data = {"test": "data", "timestamp": self._get_timestamp()}
            
            # Encriptar
            encrypted = self.encrypt_sensitive_data(test_data)
            
            # Desencriptar
            decrypted = self.decrypt_sensitive_data(encrypted)
            
            # Verificar integridad
            integrity_ok = test_data == decrypted
            
            return {
                'encryption_working': integrity_ok,
                'test_data': test_data,
                'decrypted_data': decrypted,
                'integrity_check': integrity_ok,
                'timestamp': self._get_timestamp()
            }
            
        except Exception as e:
            return {
                'encryption_working': False,
                'error': str(e),
                'timestamp': self._get_timestamp()
            }

# Función de utilidad para usar el sistema de encriptación
def get_data_encryption() -> DataEncryption:
    """Obtener instancia del sistema de encriptación"""
    if 'data_encryption' not in st.session_state:
        st.session_state['data_encryption'] = DataEncryption()
    return st.session_state['data_encryption']
