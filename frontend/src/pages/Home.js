import React, { useEffect, useState } from 'react';

function Home() {
  const [matches, setMatches] = useState([]);

  useEffect(() => {
    fetch('/matches/')
      .then(res => res.json())
      .then(data => setMatches(data));
  }, []);

  return (
    <div>
      <h1>Matchs</h1>
      <ul>
        {matches.map(m => (
          <li key={m.id}>
            {m.team_a.name} vs {m.team_b.name} le {new Date(m.date).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Home;
