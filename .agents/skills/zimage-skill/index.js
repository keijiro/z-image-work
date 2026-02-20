import axios from "axios";

const API_URL = "https://api-inference.modelscope.ai/v1/images/generations";

async function generateImage({
  prompt,
  width = 1024,
  height = 1024,
  steps = 6,
  negativePrompt
}) {
  const token = process.env.MODELSCOPE_API_TOKEN;

  if (!token) {
    throw new Error(
      "MODELSCOPE_API_TOKEN environment variable is not set."
    );
  }

  const payload = {
    model: "Tongyi-MAI/Z-Image-Turbo",
    prompt,
    size: `${width}x${height}`,
    steps
  };

  if (negativePrompt?.trim())
    payload.negative_prompt = negativePrompt;

  try {
    const response = await axios.post(
      API_URL,
      payload,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      }
    );

    return response.data;
  } catch (error) {
    console.error("Image generation failed:", error.response?.data || error.message);
    throw error;
  }
}

function parseCLIArgs() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error(
      "Usage: node index.js \"prompt\" [width] [height] [steps] [negativePrompt]"
    );
    process.exit(1);
  }

  const prompt = args[0];
  const width = args[1] ? parseInt(args[1], 10) : 1024;
  const height = args[2] ? parseInt(args[2], 10) : 1024;
  const steps = args[3] ? parseInt(args[3], 10) : 30;
  const negativePrompt = args[4];

  return { prompt, width, height, steps, negativePrompt };
}

// CLI execution mode
if (import.meta.url === `file://${process.argv[1]}`) {
  const options = parseCLIArgs();

  generateImage(options)
    .then(data => {
      console.log(JSON.stringify(data, null, 2));
    })
    .catch(() => {
      process.exit(1);
    });
}

export { generateImage };
