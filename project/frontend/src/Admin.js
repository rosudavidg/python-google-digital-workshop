import axios from "axios"
import { useState, useEffect } from 'react';
import { useHistory } from "react-router-dom";
import { Button, Card } from 'react-bootstrap';
import "./Admin.css"

const Company = ({ id, name, approved, history }) => {
    const approveCompany = () => {
        axios
            .post(`http://localhost:5000/api/companies/${id}/approve`, {}, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            })
            .then((res) => {
                history.go(0)
            })
            .catch((e) => {
                alert(`Failed to approve company: ${e.response.data.error_message}`);
            });
    }

    return <div className="company">
        <Card
            bg=""
            text="nk"
            style={{ width: '18rem' }}
            className="mb-2"
        >
            <Card.Header>Company</Card.Header>
            <Card.Body>
                <Card.Title> {name} </Card.Title>

                {!approved &&
                    <Button variant="success" type="submit" className="company-approve" onClick={approveCompany}>
                        Approve
                    </Button>
                }
            </Card.Body>
        </Card>
    </div>
}

const Admin = () => {
    const [companies, setCompanies] = useState([])
    const history = useHistory();

    const onLoadComponent = () => {
        axios
            .get('http://localhost:5000/api/companies', {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            })
            .then((res) => {
                setCompanies(res.data)
            })
            .catch((e) => {
                alert(`Failed to fetch data: ${e.response.data.error_message}`);
            });
    }

    useEffect(() => {
        onLoadComponent();
    }, [])

    return <div className="home-admin">
        <div className="home-admin-not-approved">
            {companies.filter(company => !company.approved).map(company => {
                return <Company key={company.id} id={company.id} name={company.company_name} approved={company.approved} history={history} />
            })}
        </div>
        <div className="home-admin-approved">
            {companies.filter(company => company.approved).map(company => {
                return <Company key={company.id} id={company.id} name={company.company_name} approved={company.approved} />
            })}
        </div>
    </div>
}

export default Admin
