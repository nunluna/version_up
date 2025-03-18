import requests
from bs4 import BeautifulSoup
from functools import lru_cache
import os
import time

# Настройка GitHub токена
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "your_token_here")
if GITHUB_TOKEN == "your_token_here":
    print("Предупреждение: GitHub токен не настроен! Укажи GITHUB_TOKEN в переменной окружения.")
GITHUB_HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN and GITHUB_TOKEN != "your_token_here" else None
}

# Фallback-версии (актуальные на момент 17 марта 2025 или последние известные)
FALLBACK_VERSIONS = {
    "visual studio code": "1.89.0",
    "pycharm": "2024.3.4",
    "git": "2.49.0",
    "node.js": "20.15.0",
    "python": "3.13.2",
    "docker": "25.0.3",
    "kubernetes": "1.30.0",
    "intellij idea": "2024.3.4.1",
    "webstorm": "2024.3.5",
    "ruby": "3.4.2",
    "rails": "7.1.0",
    "php": "8.2.0",
    "laravel": "10.48.0",
    "java": "23.0.2",
    "android studio": "2023.1.1"
}

@lru_cache(maxsize=128, typed=False)
def fetch_latest_version_cached(software_name):
    """
    Получает актуальную версию программного обеспечения с официальных источников.
    Возвращает строку с версией или fallback-версию в случае ошибки.
    """
    try:
        name_lower = software_name.lower()
        if name_lower in ["visual studio code", "node.js", "docker", "kubernetes", "rails", "laravel", "git"]:
            url = {
                "visual studio code": "https://api.github.com/repos/microsoft/vscode/releases/latest",
                "node.js": "https://api.github.com/repos/nodejs/node/releases/latest",
                "docker": "https://api.github.com/repos/docker/docker-ce/releases/latest",
                "kubernetes": "https://api.github.com/repos/kubernetes/kubernetes/releases/latest",
                "rails": "https://api.github.com/repos/rails/rails/releases/latest",
                "laravel": "https://api.github.com/repos/laravel/laravel/releases/latest",
                "git": "https://api.github.com/repos/git-for-windows/git/releases/latest"
            }[name_lower]
            response = requests.get(url, headers=GITHUB_HEADERS, timeout=10)
            response.raise_for_status()
            data = response.json()
            version = data.get("tag_name", "").lstrip("v")
            if name_lower == "git":
                version = ".".join(version.split(".")[:3]) if version else ""
            time.sleep(1)  # Задержка между запросами
            return version if version else FALLBACK_VERSIONS.get(name_lower, "Неизвестно")

        elif name_lower == "pycharm":
            url = "https://data.services.jetbrains.com/products/releases?code=PCP&latest=true&type=release"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()["PCP"][0]["version"]

        elif name_lower == "python":
            url = "https://www.python.org/downloads/"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            version = soup.find("a", class_="button")["href"].split('/')[-2]
            return version if version else FALLBACK_VERSIONS.get(name_lower, "3.12.0")

        elif name_lower == "intellij idea":
            url = "https://data.services.jetbrains.com/products/releases?code=IIU&latest=true&type=release"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()["IIU"][0]["version"]

        elif name_lower == "webstorm":
            url = "https://data.services.jetbrains.com/products/releases?code=WS&latest=true&type=release"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()["WS"][0]["version"]

        elif name_lower == "ruby":
            url = "https://www.ruby-lang.org/en/downloads/"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            version = soup.find("a", href=lambda x: x and "ruby-" in x).text.split()[-1]
            return version if version else FALLBACK_VERSIONS.get(name_lower, "3.2.0")

        elif name_lower == "php":
            url = "https://www.php.net/downloads.php"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            version_element = soup.find("a", class_="download-link")
            return version_element.text.split()[1] if version_element else FALLBACK_VERSIONS.get(name_lower, "8.2.0")

        elif name_lower == "java":
            for version_num in [23, 21, 17]:
                url = f"https://api.adoptium.net/v3/assets/latest/{version_num}/hotspot"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                version_data = response.json()
                if version_data and len(version_data) > 0:
                    return version_data[0]["version"]["semver"].split("+")[0]  # Убираем +7
            return FALLBACK_VERSIONS.get(name_lower, "17.0.0")

        elif name_lower == "android studio":
            url = "https://developer.android.com/studio/releases"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            version_element = soup.find("h2", class_="release-note-version")
            return version_element.text.strip() if version_element else FALLBACK_VERSIONS.get(name_lower, "2023.1.1")

        else:
            return "Неизвестно"
    except Exception as e:
        print(f"Error fetching version for {software_name}: {e}")
        return FALLBACK_VERSIONS.get(name_lower, "Неизвестно")

if __name__ == "__main__":
    # Тестовый запуск модуля
    print(f"Visual Studio Code\nАктуальная версия: {fetch_latest_version_cached('Visual Studio Code')}")
    print(f"PyCharm\nАктуальная версия: {fetch_latest_version_cached('PyCharm')}")
    print(f"Git\nАктуальная версия: {fetch_latest_version_cached('Git')}")
    print(f"Node.js\nАктуальная версия: {fetch_latest_version_cached('Node.js')}")
    print(f"Python\nАктуальная версия: {fetch_latest_version_cached('Python')}")
    print(f"Docker\nАктуальная версия: {fetch_latest_version_cached('Docker')}")
    print(f"Kubernetes\nАктуальная версия: {fetch_latest_version_cached('Kubernetes')}")
    print(f"IntelliJ IDEA\nАктуальная версия: {fetch_latest_version_cached('IntelliJ IDEA')}")
    print(f"WebStorm\nАктуальная версия: {fetch_latest_version_cached('WebStorm')}")
    print(f"Ruby\nАктуальная версия: {fetch_latest_version_cached('Ruby')}")
    print(f"Rails\nАктуальная версия: {fetch_latest_version_cached('Rails')}")
    print(f"PHP\nАктуальная версия: {fetch_latest_version_cached('PHP')}")
    print(f"Laravel\nАктуальная версия: {fetch_latest_version_cached('Laravel')}")
    print(f"Java\nАктуальная версия: {fetch_latest_version_cached('Java')}")
    print(f"Android Studio\nАктуальная версия: {fetch_latest_version_cached('Android Studio')}")