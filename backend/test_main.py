# test_main.py — Tests automatisés pour l'API
# On utilise pytest + TestClient de FastAPI pour simuler des requêtes HTTP
# Lance les tests avec : uv run pytest

from fastapi.testclient import TestClient

from main import app

# TestClient simule un navigateur/curl — il envoie des requêtes HTTP à l'app
# sans avoir besoin de lancer le serveur
client = TestClient(app)


def test_get_tasks():
    """Vérifie que GET /api/tasks retourne une liste de tâches."""
    response = client.get("/api/tasks")
    assert response.status_code == 200  # 200 = OK
    assert isinstance(response.json(), list)  # La réponse est une liste
    assert len(response.json()) >= 1  # Il y a au moins 1 tâche (les tâches de démo)


def test_create_task():
    """Vérifie que POST /api/tasks crée une tâche et retourne 201."""
    response = client.post("/api/tasks", json={"title": "Nouvelle tâche"})
    assert response.status_code == 201  # 201 = Created
    data = response.json()
    assert data["title"] == "Nouvelle tâche"
    assert data["done"] is False  # Une nouvelle tâche n'est pas terminée


def test_toggle_task():
    """Vérifie que PATCH /api/tasks/{id} inverse le statut done."""
    # Créer une tâche pour le test
    create = client.post("/api/tasks", json={"title": "À toggler"})
    task_id = create.json()["id"]

    # Premier toggle : False → True
    response = client.patch(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["done"] is True

    # Deuxième toggle : True → False
    response = client.patch(f"/api/tasks/{task_id}")
    assert response.json()["done"] is False


def test_toggle_task_not_found():
    """Vérifie que PATCH sur un ID inexistant retourne 404."""
    response = client.patch("/api/tasks/99999")
    assert response.status_code == 404  # 404 = Not Found


def test_delete_task():
    """Vérifie que DELETE /api/tasks/{id} supprime bien la tâche."""
    # Créer une tâche puis la supprimer
    create = client.post("/api/tasks", json={"title": "À supprimer"})
    task_id = create.json()["id"]

    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 204  # 204 = No Content (supprimé, rien à retourner)

    # Vérifier qu'elle n'existe plus dans la liste
    tasks = client.get("/api/tasks").json()
    assert all(t["id"] != task_id for t in tasks)


def test_delete_task_not_found():
    """Vérifie que DELETE sur un ID inexistant retourne 404."""
    response = client.delete("/api/tasks/99999")
    assert response.status_code == 404


def test_health():
    """Vérifie que le health check répond OK."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
