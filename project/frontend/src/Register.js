import "./Register.css"
import { Form, Button, Spinner } from 'react-bootstrap';
import { useHistory } from "react-router-dom";
import { useState } from 'react';
import axios from "axios";

const Register = () => {
    const [email, setEmail] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [password, setPassword] = useState('');
    const [companyName, setCompanyName] = useState('');
    const [phone, setPhone] = useState('');
    const history = useHistory();

    const onChangeEmail = (event) => {
        event.preventDefault();
        setEmail(event.target.value);
    };

    const onChangeFirstName = (event) => {
        event.preventDefault();
        setFirstName(event.target.value);
    };

    const onChangeLastName = (event) => {
        event.preventDefault();
        setLastName(event.target.value);
    };

    const onChangeCompanyName = (event) => {
        event.preventDefault();
        setCompanyName(event.target.value);
    };

    const onChangePassword = (event) => {
        event.preventDefault();
        setPassword(event.target.value);
    };

    const onChangePhone = (event) => {
        event.preventDefault();
        setPhone(event.target.value);
    };

    const onClickSubmit = (event) => {
        event.preventDefault()

        axios
            .post('http://localhost:5000/api/companies', {
                email, 'company_name': companyName, 'first_name': firstName, 'last_name': lastName, phone, password
            })
            .then((res) => {
                alert(`Successfully register. Please check your email and activate your account`);
                history.push('/login')
            })
            .catch((e) => {
                alert(`Register failed: ${e.response.data.error_message}`);
            });
    }

    return <div className="register">
        <Form onSubmit={onClickSubmit} className="custom-card-register">
            <Form.Group controlId="formGridFirstName">
                <Form.Label>First name</Form.Label>
                <Form.Control type="text" placeholder="Enter first name" onChange={onChangeFirstName} value={firstName} />
            </Form.Group>
            <Form.Group controlId="formGridLastName">
                <Form.Label>Last name</Form.Label>
                <Form.Control type="text" placeholder="Enter last name" onChange={onChangeLastName} value={lastName} />
            </Form.Group>
            <Form.Group controlId="formGridEmail">
                <Form.Label>Email</Form.Label>
                <Form.Control type="email" placeholder="Enter email" onChange={onChangeEmail} value={email} />
            </Form.Group>
            <Form.Group controlId="formGridPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Password" onChange={onChangePassword} value={password} />
            </Form.Group>
            <Form.Group controlId="formGridCompanyName">
                <Form.Label>Company name</Form.Label>
                <Form.Control type="text" placeholder="Enter company name" onChange={onChangeCompanyName} value={companyName} />
            </Form.Group>
            <Form.Group controlId="formGridPhone">
                <Form.Label>Phone</Form.Label>
                <Form.Control type="text" placeholder="Enter phone number" onChange={onChangePhone} value={phone} />
            </Form.Group>

            <Button variant="success" type="submit" className="register-success">
                Register
            </Button>
        </Form>

        <Button variant="dark" type="submit" className="register-go-back" onClick={e => { history.goBack() }}>
            Back
        </Button>
    </div>
}

export default Register