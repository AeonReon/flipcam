// Returns a stamp that changes on every Vercel deploy.
// Used by the client to detect a fresh deploy and offer a one-tap reload.
export default function handler(req, res) {
  const stamp = process.env.VERCEL_GIT_COMMIT_SHA || process.env.VERCEL_DEPLOYMENT_ID || String(Date.now());
  res.setHeader('Cache-Control', 'no-store');
  res.status(200).json({ stamp });
}
