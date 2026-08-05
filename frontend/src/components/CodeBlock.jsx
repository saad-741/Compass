import React, { useEffect, useRef } from 'react';
import hljs from 'highlight.js';
import 'highlight.js/styles/github-dark.css';

export default function CodeBlock({ language, value }) {
  const codeRef = useRef(null);

  useEffect(() => {
    if (codeRef.current) {
      hljs.highlightElement(codeRef.current);
    }
  }, [value, language]);

  return (
    <pre className="rounded-lg bg-slate-900 p-4 overflow-x-auto text-sm my-3 border border-slate-700">
      <code ref={codeRef} className={`language-${language || 'text'}`}>
        {value}
      </code>
    </pre>
  );
}