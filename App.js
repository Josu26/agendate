import React from 'react';
import './App.css';
import worldIcon from './world-icon.svg';
import contactIcon from './contact-icon.svg';

// Componente del encabezado
const Header = () => {
  return (
    <header className="header">
      <div className="logo-container">
        <img src="/logo.png" alt="AgenDate Logo" className="logo" />
      </div>
      <div className="header-icons">
        <img src={worldIcon} alt="Change Language" className="icon" />
        <img src={contactIcon} alt="Contact" className="icon" />
      </div>
    </header>
  );
};

// Componente del cuadro de botones
const ButtonBox = () => {
  return (
    <div className="button-box">
      <button className="button">Iniciar sesión</button>
      <button className="button">Registrarse</button>
    </div>
  );
};

// Componente principal de la página de inicio
const HomePage = () => {
  return (
    <div className="home-page">
      <Header />
      <div className="content">
        <div className="background">
          <div className="white-box">
            <ButtonBox />
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
