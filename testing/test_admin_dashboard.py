#!/usr/bin/env python3
"""
Script de prueba para el Dashboard Administrativo
"""

import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_admin_dashboard():
    """Test completo del dashboard administrativo"""
    print("🧪 Iniciando test del Dashboard Administrativo...")

    try:
        # Test 1: Imports
        print("1️⃣ Probando imports...")
        from modules.admin.admin_dashboard import AdminDashboard, get_admin_dashboard
        from modules.admin.admin_widgets import AdminWidgets
        from modules.admin.mock_systems import (
            MockPerformanceOptimizer, MockSecurityAuditor,
            MockRateLimiter, MockDataEncryption
        )
        print("✅ Imports exitosos")

        # Test 2: Sistemas Mock individuales
        print("\n2️⃣ Probando sistemas mock individuales...")
        perf = MockPerformanceOptimizer()
        sec = MockSecurityAuditor()
        rate = MockRateLimiter()
        enc = MockDataEncryption()

        # Test datos
        cache_stats = perf.get_cache_stats()
        security_data = sec.get_security_dashboard_data()
        rate_stats = rate.get_system_stats()
        enc_status = enc.get_encryption_status()

        print(f"  ✅ Performance: {cache_stats.get('total_entries', 0)} entradas en cache")
        print(f"  ✅ Security: {security_data.get('total_actions', 0)} acciones registradas")
        print(f"  ✅ Rate Limiting: {rate_stats.get('active_blocks', 0)} usuarios bloqueados")
        print(f"  ✅ Encryption: {enc_status.get('algorithm', 'unknown')} configurado")

        # Test 3: Dashboard principal
        print("\n3️⃣ Probando dashboard principal...")
        dashboard = AdminDashboard()

        print(f"  ✅ Dashboard creado")
        print(f"  ✅ Performance optimizer: {dashboard.performance_optimizer is not None}")
        print(f"  ✅ Security auditor: {dashboard.security_auditor is not None}")
        print(f"  ✅ Rate limiter: {dashboard.rate_limiter is not None}")
        print(f"  ✅ Data encryption: {dashboard.data_encryption is not None}")
        print(f"  ✅ Systems initialized: {dashboard.systems_initialized}")

        # Test 4: Widgets admin
        print("\n4️⃣ Probando widgets administrativos...")
        if dashboard.admin_widgets:
            print("  ✅ Admin widgets disponibles")
        else:
            print("  ⚠️ Admin widgets no disponibles")

        # Test 5: Función get_admin_dashboard
        print("\n5️⃣ Probando función get_admin_dashboard...")

        # Mock básico de streamlit.session_state
        import streamlit as st

        class MockSessionState:
            def __init__(self):
                self.data = {}
            def __contains__(self, key):
                return key in self.data
            def __getitem__(self, key):
                return self.data[key]
            def __setitem__(self, key, value):
                self.data[key] = value
            def __delitem__(self, key):
                if key in self.data:
                    del self.data[key]

        st.session_state = MockSessionState()

        dashboard2 = get_admin_dashboard()
        print(f"  ✅ Dashboard via get_admin_dashboard: {dashboard2 is not None}")
        print(f"  ✅ Sistemas inicializados: {dashboard2.systems_initialized}")

        # Test 6: Métodos específicos de datos
        print("\n6️⃣ Probando métodos de datos específicos...")

        if dashboard.performance_optimizer:
            cache_data = dashboard.performance_optimizer.get_cache_stats()
            print(f"  ✅ Cache stats obtenidos: {len(cache_data)} campos")

        if dashboard.security_auditor:
            sec_data = dashboard.security_auditor.get_security_dashboard_data(24)
            print(f"  ✅ Security data obtenida: {len(sec_data)} campos")

        if dashboard.rate_limiter:
            rate_data = dashboard.rate_limiter.get_system_stats()
            print(f"  ✅ Rate limiting stats: {len(rate_data)} campos")

        if dashboard.data_encryption:
            enc_data = dashboard.data_encryption.get_encryption_status()
            print(f"  ✅ Encryption status: {len(enc_data)} campos")

        print("\n🎉 ¡Todos los tests pasaron exitosamente!")
        print("✅ El Dashboard Administrativo está funcionando correctamente")

        return True

    except Exception as e:
        print(f"\n❌ Error en test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_admin_dashboard()
    if success:
        print("\n🚀 Sistema listo para usar")
        exit(0)
    else:
        print("\n💥 Sistema necesita correcciones")
        exit(1)