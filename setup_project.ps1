# Create directory structure
$rootDir = "C:\API_Scraping_App"
$dirs = @(
    "ai_workers",
    "tests",
    "config",
    "services",
    "logs"
)

foreach ($dir in $dirs) {
    New-Item -Path "$rootDir\$dir" -ItemType Directory -Force
}

# Create initial Python files
$files = @{
    "ai_workers\code_custodian.py" = @"
from transformers import AutoModelForCausalLM, AutoTokenizer

class CodeCustodianAI:
    def __init__(self, model_name="codellama/code-llama-small"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto"
        )
    
    def analyze_and_fix_code(self, code_snippet):
        # Implementation coming soon
        pass
"@

    "tests\test_code_custodian.py" = @"
import pytest
from ai_workers.code_custodian import CodeCustodianAI

def test_code_custodian_initialization():
    custodian = CodeCustodianAI()
    assert custodian is not None
"@

    "services\rabbitmq_service.py" = @"
import pika

class RabbitMQService:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )
        self.channel = self.connection.channel()
"@
}

foreach ($file in $files.Keys) {
    $content = $files[$file]
    $filePath = Join-Path $rootDir $file
    New-Item -Path $filePath -ItemType File -Force
    Set-Content -Path $filePath -Value $content
}

# Create requirements.txt
$requirements = @"
transformers
torch
pika
pytest
flake8
python-dotenv
"@
Set-Content -Path "$rootDir\requirements.txt" -Value $requirements

# Create .env file
$envContent = @"
MODEL_NAME=codellama/code-llama-small
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_MANAGEMENT_PORT=15672
"@
Set-Content -Path "$rootDir\.env" -Value $envContent