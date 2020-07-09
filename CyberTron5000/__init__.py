from CyberTron5000.CyberTron5000.ct5k import client


def get_token():
    with open("secrets.txt", "r") as f:
        secrets = f.readlines()
        return secrets[0].strip()


client.run(get_token())
