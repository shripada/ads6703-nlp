// All calls to the back end go through here. The Groq key is never in this code: the back end holds it.
async function call(path, options = {}) {
  const res = await fetch(`/api${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail ?? `Request failed (${res.status})`);
  return data;
}

export const listTexts = () => call("/texts");
export const addText = (body) => call("/texts", { method: "POST", body: JSON.stringify({ body }) });
export const ask = (question) => call("/ask", { method: "POST", body: JSON.stringify({ question }) });
