#!/bin/bash
#
# Salesforce Data Loader Password Encryption Utility
# Usage: ./encrypt_password.sh "YOUR_PASSWORD"
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DATALOADER_JAR="${SCRIPT_DIR}/dataloader-64.1.0.jar"

if [ -z "$1" ]; then
    echo "Usage: $0 <password_to_encrypt>"
    echo ""
    echo "Example:"
    echo "  $0 'MySecretPassword123'"
    exit 1
fi

# Check Java
if ! command -v java &> /dev/null; then
    echo "Error: Java is not installed or not in PATH"
    echo "Please install Java 17 or later"
    exit 1
fi

echo "Encrypting password..."
echo ""
java --enable-native-access=ALL-UNNAMED -cp "${DATALOADER_JAR}" com.salesforce.dataloader.security.EncryptionUtil -e "$1"
echo ""
echo "Copy the encrypted string above and paste it into your airflow_variables.json"
