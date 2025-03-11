import requests
from bs4 import BeautifulSoup

def fetch_latest_version(software_name):
    """
    Получает актуальную версию программного обеспечения с официальных источников.
    Поддерживает 15 популярных ПО через API или парсинг.
    Возвращает строку с версией или "Unknown" в случае ошибки.
    """
    try:
        name_lower = software_name.lower()
        if name_lower == "visual studio code":
            url = "https://api.github.com/repos/microsoft/vscode/releases/latest"
            response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"})
            return response.json()["tag_name"].lstrip("v")

        elif name_lower == "pycharm":
            url = "https://data.services.jetbrains.com/products/releases?code=PCP&latest=true&type=release"
            response = requests.get(url)
            return response.json()["PCP"][0]["version"]

        elif name_lower == "git":
            url = "https://api.github.com/repos/git-for-windows/git/releases/latest"
            response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"})
            return response.json()["tag_name"].split("-")[-1]

        elif name_lower == "node.js":
            url = "https://api.github.com/repos/nodejs/node/releases/latest"
            response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"})
            return response.json()["tag_name"].lstrip("v")

        elif name_lower == "python":
            url = "https://www.python.org/downloads/"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.find("a", class_="button")["href"].split('/')[-2]

        elif name_lower == "docker":
            url = "https://api.github.com/repos/docker/docker-ce/releases/latest"
            response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"})
            return response.json()["tag_name"].lstrip("v")

        elif name_lower == "kubernetes":
            url = "https://api.github.com/repos/kubernetes/kubernetes/releases/latest"
            response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"})
            return response.json()["tag_name"].lstrip("v")

        elif name_lower == "intellij idea":
            url = "https://data.services.jetbrains.com/products/releases?code=IIU&latest=true&type=release"
            response = requests.get(url)
            return response.json()["IIU"][0]["version"]

        elif name_lower == "webstorm":
            url = "https://data.services.jetbrains.com/products/releases?code=WS&latest=true&type=release"
            response = requests.get(url)
            return response.json()["WS"][0]["version"]

        elif name_lower == "ruby":
            url = "https://www.ruby-lang.org/en/downloads/"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.find("a", href=lambda x: x and "ruby-" in x).text.split()[-1]

        elif name_lower == "rails":
            url = "https://api.github.com/repos/rails/rails/releases/latest"
            response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"})
            return response.json()["tag_name"].lstrip("v")

        elif name_lower == "php":
            url = "https://www.php.net/downloads.php"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            version_element = soup.find("a", class_="download-link")
            if version_element:
                return version_element.text.split()[1]
            else:
                return "Неизвестно"

        elif name_lower == "laravel":
            url = "https://api.github.com/repos/laravel/laravel/releases/latest"
            response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"})
            return response.json()["tag_name"].lstrip("v")

        elif name_lower == "java":
            url = "https://www.oracle.com/java/technologies/javase-downloads.html"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            version_element = soup.find("h3", text=lambda t: "JDK" in t)
            if version_element:
                return version_element.text.split()[-1]
            else:
                return "Неизвестно"

        elif name_lower == "android studio":
            url = "https://developer.android.com/studio/releases"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            version_element = soup.find("h2", class_="release-note-version")
            if version_element:
                return version_element.text.strip()
            else:
                return "Неизвестно"

        else:
            return "Unknown"
    except Exception as e:
        print(f"Error fetching version for {software_name}: {e}")
        return "Unknown"

if __name__ == "__main__":
    # Тестовый запуск модуля
    print(fetch_latest_version("Visual Studio Code"))
    print(fetch_latest_version("PyCharm"))
    print(fetch_latest_version("Git"))
    print(fetch_latest_version("PHP"))
    print(fetch_latest_version("Android Studio"))
    print(fetch_latest_version("Java"))
