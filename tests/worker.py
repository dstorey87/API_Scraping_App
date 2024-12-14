import logging
from ai_workers.code_custodian import CodeCustodianAI
from services.rabbitmq_service import RabbitMQService
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalysisWorker:
    def __init__(self):
        self.custodian = CodeCustodianAI()
        self.rabbitmq = RabbitMQService()
        
    def process_message(self, ch, method, properties, body):
        try:
            data = json.loads(body)
            code = data['code']
            result = self.custodian.analyze_and_fix_code(code)
            logger.info(f"Processed code analysis: {result}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def start(self):
        logger.info("Starting analysis worker...")
        self.rabbitmq.process_tasks(self.process_message)

if __name__ == "__main__":
    worker = AnalysisWorker()
    worker.start()