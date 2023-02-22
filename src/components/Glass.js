import './Glass.css';
import { useState } from 'react';
import axios from 'axios';
import validator from "validator";

function Glass() {
  const [url, setUrl] = useState('');
  const [prediction, setPrediction] = useState('');
  const [interpretation, setInterpretation] = useState('');
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validator.isURL(url)) {
      setError("Invalid URL");
      return;
    }
    const params = { url };
    axios
      .post('http://localhost:8080/prediction', params)
      .then((res) => {
        const data = res.data.data;
        const parameters = JSON.stringify(params);
        const msg = `Prediction: ${data.prediction}\nInterpretation: ${data.interpretation}\nParameters: ${parameters}`;
        setPrediction(data.prediction);
        setInterpretation(data.interpretation);
        reset();
      })
      .catch((error) => setError(`Error: ${error.message}`));
  };

  const reset = () => {
    setUrl('');
  };

  return (
    <div className="glass">
      <form onSubmit={handleSubmit} className="glass__form">
        <div className="title">
          <h4>Malicious URL</h4>
          <h4 id="style__text">detection</h4>
          <h3>Never fall for a phishing link again.</h3>
        </div>
        <div className="glass__form__group">
          <input
            autocomplete="off"
            id="url"
            className={`glass__form__input ${prediction === 'phishing' ? 'phishing__input' : 'legitimate__input'}`}
            placeholder="Enter URL"
            required
            autoFocus
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            onFocus={() => {setError(''); setInterpretation(''); setPrediction('');}}
        
          />
          {error && <span className="error">{error}</span>}
        </div>

        <div className="glass__form__group">
          <button type="submit" className="glass__form__btn">
            Submit
          </button>
          <span className={prediction === 'phishing' ? 'phishing' : 'legitimate'}>
          {interpretation}
          </span>
        </div>
      </form>
    </div>
  );
}

export default Glass;
