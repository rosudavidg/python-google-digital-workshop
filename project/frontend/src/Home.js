import { Form, Button, Spinner } from 'react-bootstrap';
import { useHistory } from "react-router-dom";
import { useState } from 'react';
import "./Home.css"
import axios from "axios";
import Admin from "./Admin"
import Company from "./Company"
import Employee from "./Employee"
import jwt_decode from "jwt-decode";

const isAdminUser = () => {
    return jwt_decode(localStorage.getItem("token")).role_name == "admin";
}

const isCompanyUser = () => {
    return jwt_decode(localStorage.getItem("token")).role_name == "company";
}

const isEmployeeUser = () => {
    return jwt_decode(localStorage.getItem("token")).role_name == "employee";
}

const LogOut = ({ setIsLoggedIn, history }) => {
    const onClick = () => {
        setIsLoggedIn(false)
        localStorage.removeItem('token')
        history.go(0)
    }

    return <Button variant="dark" type="submit" className="home-page-register-button" onClick={onClick}>
        Log out
    </Button>
}

const Home = ({ setIsLoggedIn }) => {
    const history = useHistory();

    return <div className="home-view">
        {isAdminUser() && <Admin />}
        {isCompanyUser() && <Company />}
        {isEmployeeUser() && <Employee />}
        <LogOut setIsLoggedIn={setIsLoggedIn} history={history} />
    </div>
}

export default Home
