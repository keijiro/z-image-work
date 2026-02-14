import axios from "axios";

const API_URL = "https://api-inference.modelscope.ai/v1/images/generations";

/**
 * Generate an image using ModelScope Z-Image API.
 *
 * @param {Object} options
 * @param {string} options.prompt - Text prompt for image generation
 * @param {number} [options.width=1024] - Output image width
 * @param {number} [options.height=1024] - Output image height
 * @param {number} [options.steps=30] - Number of diffusion steps
 * @returns {Promise<Object>} API response data
 */
async function generateImage({
  prompt,
  width = 1024,
  height = 1024,
  steps = 6
}) {
  const token = process.env.MODELSCOPE_API_KEY;

  if (!token) {
    throw new Error("MODELSCOPE_API_KEY environment variable is not set.");
  }

  try {
    const response = await axios.post(
      API_URL,
      {
        model: "Tongyi-MAI/Z-Image-Turbo",
        prompt,
        width,
        height,
        steps
      },
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

/**
 * Parse CLI arguments into generation options.
 *
 * Example:
 * node index.js "a cat portrait" 512 512 40
 */
function parseCLIArgs() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error("Usage: node index.js \"prompt\" [width] [height] [steps]");
    process.exit(1);
  }

  const prompt = args[0];
  const width = args[1] ? parseInt(args[1], 10) : 1024;
  const height = args[2] ? parseInt(args[2], 10) : 1024;
  const steps = args[3] ? parseInt(args[3], 10) : 30;

  return { prompt, width, height, steps };
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
