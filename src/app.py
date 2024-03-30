from flask import Flask, jsonify, request
import requests, yaml, re
import os

icons = {
    "nginx": "php.png",
    "mailu": "mailu.png",
    "traefik": "traefik.png",
    "portainer": "portainer.png",
    "phpmyadmin": "phpmyadmin.png",
    "crontab": "crontab-ui.png",
}

homepage_path = os.getenv("HOMEPAGE_PATH", "homepage/config/services.yaml")
pattern = r"Host\([^)]*\)"
app = Flask(__name__)


def is_custom_service(rule):
    return re.search(pattern, rule) is not None


##* APIs *##
@app.route("/api/v1/homepage/update", methods=["PUT"])
def homepage_update():
    # Open the YAML file for reading
    with open(str(homepage_path), "r") as yaml_file:
        data = yaml.safe_load(yaml_file)

    response = requests.get(
        "http://web1.elemento.cloud:8080/api/http/routers"
    )  # ToDo: generalize the URL of traefik

    routers = response.json()
    keys = [list(service.keys())[0] for service in data[0]["Services"]]
    for router in routers:
        name = router["name"].split("@")[0]
        if (
            is_custom_service(router["rule"])
            and name.capitalize() not in keys
            and name != "homepage"
        ):
            icon = icons[name] if name in icons else ""
            data[0]["Services"].append(
                {
                    name.capitalize(): {
                        "icon": icon,
                        "href": "http://" + router["rule"].split("`")[1],
                    }
                }
            )

    with open("test.yaml", "w") as yaml_file:
        yaml.dump(data, yaml_file)


##* APP (just for testing purpose - use flask run instead) *##
if __name__ == "__main__":
    # app.run(port=5001, debug=True)
    homepage_update()
