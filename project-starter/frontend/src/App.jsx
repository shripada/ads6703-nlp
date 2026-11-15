// A small working example: label a text with BERT, and ask the LLM a question.
// Replace it with your own screens.
import { useEffect, useState } from "react";
import { addText, ask, listTexts } from "./api.js";

export default function App() {
  const [texts, setTexts] = useState([]);
  const [draft, setDraft] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    listTexts().then(setTexts).catch((e) => setError(e.message));
  }, []);

  async function onLabel(e) {
    e.preventDefault();
    setError("");
    try {
      const saved = await addText(draft);
      setTexts([saved, ...texts]);
      setDraft("");
    } catch (err) {
      setError(err.message);
    }
  }

  async function onAsk(e) {
    e.preventDefault();
    setError("");
    try {
      setAnswer((await ask(question)).answer);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <main>
      <h1>Starter app</h1>
      {error && <p className="error">{error}</p>}

      <section>
        <h2>Label a text with BERT</h2>
        <form onSubmit={onLabel}>
          <textarea value={draft} onChange={(e) => setDraft(e.target.value)} rows={3} />
          <button disabled={!draft.trim()}>Label it</button>
        </form>
        <ul>
          {texts.map((t) => (
            <li key={t.id}>
              <strong>{t.label}</strong> ({Math.round(t.score * 100)}%) {t.body}
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Ask the LLM</h2>
        <form onSubmit={onAsk}>
          <input value={question} onChange={(e) => setQuestion(e.target.value)} />
          <button disabled={!question.trim()}>Ask</button>
        </form>
        {answer && <p>{answer}</p>}
      </section>
    </main>
  );
}
