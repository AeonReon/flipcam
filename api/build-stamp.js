module.exports = function handler(req, res) {
  const stamp = process.env.VERCEL_GIT_COMMIT_SHA || process.env.VERCEL_DEPLOYMENT_ID || String(Date.now());
  res.setHeader('Cache-Control', 'no-store');
  res.status(200).json({ stamp });
};
