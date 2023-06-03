import './Nav.sass';
import Logo2 from "../../static/undraw_cabin_hkfr_red.svg";
import React from 'react';
import { Link } from 'react-router-dom';

let GIT_HUB_LINK = "https://github.com/50657472-416C6578656576/trading_bot/";

const Nav = () => {
    return (
        <div className="Nav">
            <div className="menu-btn">
                <div className="btn-burger">
                    <div className="burger-row"/>
                    <div className="burger-row"/>
                    <div className="burger-row"/>
                </div>
            </div>
            <a href="/" className='logo mobile-nav-bar'>
                <img id='big-logo-2' height={80} src={Logo2}/>
            </a>
            <nav className='nav-bar mobile-nav-bar'>
                <ul className='nav-links mobile-nav-links'>
                    <li><Link to='/control'>bot control</Link></li>
                    <li><Link to='/profile'>your account</Link></li>
                    <li><a href={GIT_HUB_LINK}>github repository</a></li>
                </ul>
            </nav>
        </div>
    )
}

export default Nav;
