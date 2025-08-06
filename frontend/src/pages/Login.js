import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    try {
      const res = await axios.post('https://fastapi-1-upuq.onrender.com/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      localStorage.setItem('token', res.data.access_token);
      navigate('/home');
    } catch (err) {
      console.error('Login failed:', err.response?.data || err.message);
      alert('Invalid credentials!');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: 'auto', marginTop: '100px' }}>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={{ display: 'block', width: '100%', marginBottom: '10px' }}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ display: 'block', width: '100%', marginBottom: '10px' }}
          required
        />
        <button type="submit" style={{ width: '100%' }}>Login</button>
      </form>
    </div>
  );
}

export default Login;
