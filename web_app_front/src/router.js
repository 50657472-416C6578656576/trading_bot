import React from 'react';
import {Route, Routes} from "react-router-dom";
import Home from "./components/Home/Home";
import Control from "./components/Control/Control";
import Profile from "./components/Profile/Profile";
import Settings from "./components/Settings/Settings";


const Router = () => {
    return (
            <Routes>
                <Route path="/" element={<Home/>}/>
                <Route path="/control" element={<Control/>}/>
                <Route path="/profile" element={<Profile/>}/>
                <Route path="/settings" element={<Settings/>}/>
            </Routes>
    );
};

export default Router;
