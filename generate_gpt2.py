import logging
import simpletransformers
from simpletransformers.language_generation import LanguageGenerationModel

logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

model = LanguageGenerationModel("gpt2", "outputs/from_scratch/best_model/", args={"max_length": 20},use_cuda=False)
# model = LanguageGenerationModel("gpt2", "outputs/fine-tuned", args={"max_length": 200})
# model = LanguageGenerationModel("gpt2", "gpt2", args={"max_length": 200})

prompts = [
    "Bonjour",
    "Ça va?"
]

for prompt in prompts:
    generated = model.generate(prompt, verbose=False)

    generated = ".".join(generated[0].split(".")[:-1]) + "."
    print("=============================================================================")
    print(generated)
    print("=============================================================================")
