import os
import subprocess

def list_certificates(jks_file, jks_password):
    # Utilisation de Popen pour exécuter la commande
    command = ["keytool", "-list", "-keystore", jks_file, "-storepass", jks_password]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if process.returncode != 0:
        print("Erreur lors de la lecture du keystore {}: {}".format(jks_file, stderr))
        return []
    
    return stdout.splitlines()

def compare_jks(jks1, jks2, password1, password2):
    certs_jks1 = list_certificates(jks1, password1)
    certs_jks2 = list_certificates(jks2, password2)

    certs_jks1_aliases = set([line.split(",")[0] for line in certs_jks1 if "PrivateKeyEntry" in line or "trustedCertEntry" in line])
    certs_jks2_aliases = set([line.split(",")[0] for line in certs_jks2 if "PrivateKeyEntry" in line or "trustedCertEntry" in line])

    missing_in_jks2 = certs_jks1_aliases - certs_jks2_aliases
    print("Certificats manquants dans {}: {}".format(jks2, missing_in_jks2))
    return missing_in_jks2

def add_certificate(jks_source, jks_target, alias, password_source, password_target):
    # Exportation du certificat
    export_cmd = ["keytool", "-exportcert", "-keystore", jks_source, "-storepass", password_source, "-alias", alias, "-file", "/tmp/{}.cer".format(alias)]
    import_cmd = ["keytool", "-importcert", "-keystore", jks_target, "-storepass", password_target, "-alias", alias, "-file", "/tmp/{}.cer".format(alias), "-noprompt"]

    subprocess.Popen(export_cmd).wait()
    subprocess.Popen(import_cmd).wait()
    
    os.remove("/tmp/{}.cer".format(alias))

def main():
    jks1 = raw_input("Chemin du premier keystore JKS: ")  # raw_input pour Python 2
    jks2 = raw_input("Chemin du second keystore JKS: ")
    password1 = raw_input("Mot de passe du premier keystore JKS: ")
    password2 = raw_input("Mot de passe du second keystore JKS: ")

    missing_certs = compare_jks(jks1, jks2, password1, password2)

    for alias in missing_certs:
        confirm = raw_input("Voulez-vous ajouter le certificat '{}' au second keystore ? (oui/non): ".format(alias)).strip().lower()
        if confirm == 'oui':
            add_certificate(jks1, jks2, alias, password1, password2)
            print("Certificat '{}' ajouté avec succès.".format(alias))
        else:
            print("Certificat '{}' non ajouté.".format(alias))

if __name__ == "__main__":
    main()
