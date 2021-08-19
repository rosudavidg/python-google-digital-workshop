import axios from "axios"
import { Form, Button, Spinner, Card } from 'react-bootstrap';
import { useState, useEffect } from 'react';
import { useHistory } from "react-router-dom";
import "./Company.css"


const Employee = ({ employee, history }) => {
    const onClickRemove = (event) => {
        event.preventDefault()

        axios
            .delete(`http://localhost:5000/api/employees/${employee.id}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            })
            .then((res) => {
                history.go(0)
            })
            .catch((e) => {
                alert(`Failed to delete employee: ${e.response.data.error_message}`);
            });
    }

    return <Card
        bg=""
        text="nk"
        // style={{ width: '18rem' }}
        className="mb-2"
    >
        <Card.Header>Employee</Card.Header>
        <Card.Body>
            <Card.Title>Email: {employee.email}</Card.Title>
            <Card.Title>First name: {employee.first_name}</Card.Title>
            <Card.Title>Last name: {employee.last_name}</Card.Title>
            <Card.Title>Phone: {employee.phone}</Card.Title>
            <Button variant="danger" type="submit" className="" onClick={onClickRemove}>
                Remove
            </Button>
        </Card.Body>
    </Card>
}


const AddEmployee = ({ history }) => {
    const [email, setEmail] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [phone, setPhone] = useState('');

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

    const onChangePhone = (event) => {
        event.preventDefault();
        setPhone(event.target.value);
    };

    const onClickSubmit = (event) => {
        event.preventDefault()

        axios
            .post('http://localhost:5000/api/accounts', {
                'accounts': [{ email, 'first_name': firstName, 'last_name': lastName, phone }]
            }, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            })
            .then((res) => {
                alert(`Employee successfully created`);
                history.go(0)
            })
            .catch((e) => {
                alert(`Creating employees failed: ${e.response.data.error_message}`);
            });
    }


    return <Card
        bg=""
        text="nk"
        style={{ width: '18rem' }}
        className="mb-2"
    >
        <Card.Header>Add Employee</Card.Header>
        <Card.Body>
            <Card.Title>Email: </Card.Title>
            <Form onSubmit={onClickSubmit} className="custom-card">
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
                <Form.Group controlId="formGridPhone">
                    <Form.Label>Phone</Form.Label>
                    <Form.Control type="text" placeholder="Enter phone number" onChange={onChangePhone} value={phone} />
                </Form.Group>

                <Button variant="primary" type="submit">
                    Add employee
            </Button>
            </Form>
        </Card.Body>
    </Card>
}

const Employees = ({ company, history }) => {
    return <div><div className="home-employees">
        {company.accounts.map((e, id) => {
            return <Employee employee={e} key={id} history={history} />
        })}
    </div>
        <div className="home-employees">
            <AddEmployee history={history} />
        </div>
    </div>
}

const ParkingLot = ({ parking_lot, history }) => {
    const onClickDelete = (event) => {
        event.preventDefault()

        axios
            .delete(`http://localhost:5000/api/parking_lots/${parking_lot.id}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            })
            .then((res) => {
                history.go(0)
            })
            .catch((e) => {
                alert(`Failed to delete parking lot: ${e.response.data.error_message}`);
            });
    }

    const onClickBlockUnblock = (event) => {
        event.preventDefault()

        const action = parking_lot.blocked ? "unblock" : "block"

        axios
            .post(`http://localhost:5000/api/parking_lots/${parking_lot.id}/${action}`, {}, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            })
            .then((res) => {
                history.go(0)
            })
            .catch((e) => {
                alert(`Failed to delete parking lot: ${e.response.data.error_message}`);
            });
    }

    return <Card
        bg={parking_lot.blocked ? "secondary" : ""}
        text="nk"
        style={{ width: '18rem' }}
        className="mb-2"
    >
        <Card.Header>Parking lot</Card.Header>
        <Card.Body>
            <Card.Title>Parking lot #{parking_lot.internal_id}</Card.Title>

            <div className="button-group">
                <Button variant={parking_lot.blocked ? "success" : "warning"} type="submit" className="company-pl-card-button" onClick={onClickBlockUnblock}>
                    {parking_lot.blocked ? "Unblock" : "Block"}
                </Button>

                <Button variant="danger" type="submit" className="company-pl-card-button" onClick={onClickDelete}>
                    Delete
            </Button>
            </div>
        </Card.Body>
    </Card>
}

const ParkingLots = ({ company, history }) => {
    const onClickDelete = (event) => {
        event.preventDefault()

        axios
            .delete(`http://localhost:5000/api/parking_lots`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            })
            .then((res) => {
                history.go(0)
            })
            .catch((e) => {
                alert(`Failed to delete parking lots: ${e.response.data.error_message}`);
            });
    }

    if (company.has_parking_lots) {
        return <div className="home-parking-lotss">
            <div className="home-parking-lots">
                {company.parking_lots.map((e, id) => {
                    return <ParkingLot parking_lot={e} key={id} history={history} />
                })}
            </div>

            <Button variant="danger" type="submit" className="company-delete-parking-lots" onClick={onClickDelete}>
                Delete all parking lots
            </Button>
        </div>
    }
    else {
        return <div></div>
    }
}

const AddParkingLots = ({ company, history }) => {
    const [startWith, setStartWith] = useState(0)
    const [parkingLotsCount, setParkingLotsCount] = useState(0)

    const onChangeStartWith = (event) => {
        event.preventDefault();
        setStartWith(event.target.value);
    };

    const onChangeParkingLotsCount = (event) => {
        event.preventDefault();
        setParkingLotsCount(event.target.value);
    };

    const onClickAdd = (event) => {
        event.preventDefault()

        axios
            .post(`http://localhost:5000/api/parking_lots`, {
                parking_lots_count: parkingLotsCount,
                begin_with: startWith
            }, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            })
            .then((res) => {
                history.go(0)
            })
            .catch((e) => {
                alert(`Failed to approve add parking lots: ${e.response.data.error_message}`);
            });
    }

    if (!company.has_parking_lots) {
        return <div>
            <Form onSubmit={onClickAdd} className="custom-card">
                <Form.Group controlId="formGridStartWith">
                    <Form.Label>Start with</Form.Label>
                    <Form.Control type="number" placeholder="Enter start number" onChange={onChangeStartWith} value={startWith} />
                </Form.Group>
                <Form.Group controlId="formGridTotalNumber">
                    <Form.Label>Number of parking lots</Form.Label>
                    <Form.Control type="number" placeholder="Enter number" onChange={onChangeParkingLotsCount} value={parkingLotsCount} />
                </Form.Group>
                <Button variant="primary" type="submit">
                    Add parking lots
            </Button>
            </Form>
        </div>
    } else {
        return <div></div>
    }
}

const Company = () => {
    const [company, setCompany] = useState({ 'accounts': [], 'parking_lots': [] })
    const history = useHistory();

    const onLoadComponent = () => {
        axios
            .get('http://localhost:5000/api/company', {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            })
            .then((res) => {
                console.log(res.data)
                setCompany(res.data)
            })
            .catch((e) => {
                alert(`Failed to fetch data: ${e.response.data.error_message}`);
            });
    }

    useEffect(() => {
        onLoadComponent();
    }, [])

    return <div className="home-company">
        <div className="section">Employees</div>
        <Employees company={company} history={history} />
        <div className="section">Parking Lots</div>
        <ParkingLots company={company} history={history} />
        <AddParkingLots company={company} history={history} />
    </div>
}

export default Company