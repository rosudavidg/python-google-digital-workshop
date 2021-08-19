import "./Login.css"
import { Form, Button, Spinner } from 'react-bootstrap';
import { useHistory } from "react-router-dom";
import { useState } from 'react';
import axios from "axios";


const Login = ({ setIsLoggedIn }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const history = useHistory();

    const onChangeEmail = (event) => {
        event.preventDefault();
        setEmail(event.target.value);
    };

    const onChangePassword = (event) => {
        event.preventDefault();
        setPassword(event.target.value);
    };

    const onClickLogin = (event) => {
        event.preventDefault()

        axios
            .post('http://localhost:5000/api/auth/login', {
                email, password
            })
            .then((res) => {
                localStorage.setItem("token", res.data.token);
                setIsLoggedIn(true)
                history.push('/')
            })
            .catch((e) => {
                alert(`Login failed: ${e.response.data.error_message}`);
            });
    }

    return <div className="login-form">
        <Form onSubmit={onClickLogin} className="custom-card-login">
            <Form.Group controlId="formGridEmail">
                <Form.Label>Email</Form.Label>
                <Form.Control type="email" placeholder="Enter email" onChange={onChangeEmail} value={email} />
            </Form.Group>
            <Form.Group controlId="formGridPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Password" onChange={onChangePassword} value={password} />
            </Form.Group>
            <Button variant="primary" type="submit">
                Login
            </Button>
        </Form>

        <Button variant="dark" type="submit" className="login-go-back" onClick={e => { history.goBack() }}>
            Back
        </Button>
    </div>
}

export default Login
