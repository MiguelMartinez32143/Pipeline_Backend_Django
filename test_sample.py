"""Pruebas de humo (smoke tests) del proyecto.

Se ejecutan en el agente de Jenkins, que solo dispone de Python + pytest
(sin Django instalado), por eso estas pruebas no importan Django: validan
la integridad del repositorio y del empaquetado antes de construir la
imagen Docker.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def test_manage_py_existe():
    """El punto de entrada de Django debe estar en la raiz del proyecto."""
    assert (BASE_DIR / "manage.py").is_file()


def test_requirements_declara_dependencias_clave():
    """La imagen no puede construirse si faltan las dependencias base."""
    requirements = (BASE_DIR / "requirements.txt").read_text(encoding="utf-8")
    for paquete in ("Django", "gunicorn", "pytest"):
        assert paquete.lower() in requirements.lower()


def test_dockerfile_es_multi_etapa():
    """La guia exige una construccion multi-stage (builder + final)."""
    dockerfile = (BASE_DIR / "dockerfile").read_text(encoding="utf-8")
    assert dockerfile.lower().count("from ") >= 2


def test_manifiestos_de_kubernetes_presentes():
    """Los cuatro manifiestos de la Fase 2 deben estar versionados."""
    esperados = {
        "backend-deployment.yaml",
        "backend-service.yaml",
        "postgres-configmap.yaml",
        "postgres-secret.yaml",
    }
    presentes = {p.name for p in (BASE_DIR / "k8s").iterdir()}
    assert esperados.issubset(presentes)
