---
name: zimage
description: Use when the user asks to generate images via ModelScope Z-Image API (Tongyi-MAI/Z-Image-Turbo); run the bundled Node.js script and require MODELSCOPE_API_TOKEN for live calls.
---

# Z-Image Generation Skill

This skill generates an image from a natural-language prompt using the ModelScope Z-Image API.

## When to use

- Generate a new image given a prompt
- Specify size (width × height)
- Control diffusion steps

## Workflow

1. Decide if the user wants an image and/or parameters.
2. Collect required inputs:
   - prompt
   - width
   - height
   - steps
   - negative prompt (optional)
3. Run the bundled Node.js script (`index.js`) with provided inputs.
4. Return the result (image URL or base64 payload) to the user.

## Default behavior

- If width or height is omitted, defaults to 1024.
- If steps is omitted, defaults to 30.
- Negative prompt is optional and passed as `negative_prompt` in API payload.
- Requires `MODELSCOPE_API_TOKEN` to be set in environment.

## Notes

- Model: `Tongyi-MAI/Z-Image-Turbo`
- API: `https://api-inference.modelscope.ai/v1/images/generations`
- Free tier and rate limits depend on ModelScope account and current policy.

## CLI Example

```bash
node index.js "a cat portrait" 512 512 30 "blurry, low quality, deformed"
```
