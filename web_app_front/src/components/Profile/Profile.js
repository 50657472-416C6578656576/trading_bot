import './Profile.sass';
import React, { useState } from 'react';
import httpClient from "../../httpClient";

const Profile = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [api_key, setApiKey] = useState("");
  const [secret, setSecret] = useState("");

  const signUpUser = async () => {
    console.log(email, password);

    try {
      const resp = await httpClient.post("/register", {
        email,
        password,
        api_key,
        secret
      });
      window.location.href = "/profile";
    } catch (error) {
      alert("Invalid credentials");
    }
  };
  const logInUser = async () => {
    console.log(email, password);

    try {
      const resp = await httpClient.post("/login", {
        email,
        password
      });

      window.location.href = "/profile";
    } catch (error) {
      alert("Invalid credentials");
    }
  };
  window.addEventListener("DOMContentLoaded", (event) => {
    const signUpButton = document.getElementById('signUp');
    const signInButton = document.getElementById('signIn');
    const container = document.getElementById('container');

    signUpButton.addEventListener('click', () => {
        container.classList.add("right-panel-active");
    });
    signInButton.addEventListener('click', () => {
        container.classList.remove("right-panel-active");
    });
  });

  return (
<div className="container-form-wrapper">
<div className="container" id="container">
    <div className="form-container sign-up-container">
        <form>
        <h1>Sign up</h1>
        <div>
          <input
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            id=""
            placeholder="email"
          />
        </div>
        <div>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            id=""
            placeholder="password"
          />
        </div>
        <div>
          <input
            type="password"
            value={api_key}
            onChange={(e) => setApiKey(e.target.value)}
            id=""
            placeholder="binance API key"
          />
        </div>
        <div>
          <input
            type="password"
            value={secret}
            onChange={(e) => setSecret(e.target.value)}
            id=""
            placeholder="binance secret"
          />
        </div>
        <br/>
        <button type="button" onClick={() => signUpUser()}>
          Submit
        </button>
      </form>
    </div>
    <div className="form-container sign-in-container">
      <form>
        <h1>Sign in</h1>
        <div>
          <input
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            id=""
            placeholder="email"
          />
        </div>
        <div>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            id=""
            placeholder="password"
          />
        </div>
        <br/>
        <button type="button" onClick={() => logInUser()}>
          Log In
        </button>
      </form>
    </div>
    <div className="overlay-container">
      <div className="overlay">
        <div className="overlay-panel overlay-left">
          <h1>Welcome Back!</h1>
          <p>To continue you should log into your account</p>
          <button className="ghost" id="signIn">Sign In</button>
        </div>
        <div className="overlay-panel overlay-right">
          <h1>Hello, Friend!</h1>
          <p>If u want to create a new account, enter you personal data and Binance info </p>
          <button className="ghost" id="signUp">Sign Up</button>
        </div>
      </div>
    </div>
  </div>
</div>
  );
};

export default Profile;
