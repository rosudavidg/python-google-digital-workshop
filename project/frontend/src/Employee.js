import axios from "axios"
import { useState, useEffect } from "react";
import { useHistory } from "react-router-dom";
import { Button, Card } from 'react-bootstrap';
import "./Employee.css"

const BookParkingLot = ({ history }) => {
    const onClickBook = (event) => {
        event.preventDefault()

        axios
            .post(`http://localhost:5000/api/parking_lot/book`, {
                date: '2021-5-29'
            }, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            })
            .then((res) => {
                history.go(0)
            })
            .catch((e) => {
                alert(`Failed to book: ${e.response.data.error_message}`);
            });
    }

    return <Button variant="success" type="submit" className="booking-button" onClick={onClickBook}>
        Book a parking lot for tomorrow
    </Button>
}

const FutureSchedule = ({ schedule, history }) => {
    const onClickCancel = (event) => {
        event.preventDefault()
        axios
            .delete(`http://localhost:5000/api/parking_lot/books/${schedule.id}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            })
            .then((res) => {
                history.go(0)
            })
            .catch((e) => {
                alert(`Failed to delete schedule: ${e.response.data.error_message}`);
            });
    }


    return <Card
        bg={""}
        text="nk"
        style={{ width: '18rem' }}
        className="mb-2"
    >
        <Card.Header>{schedule.date}</Card.Header>
        <Card.Body>
            <Card.Title>Parking lot #{schedule.internal_id}</Card.Title>

            <Button variant="danger" type="submit" className="company-approve" onClick={onClickCancel}>
                Cancel
            </Button>
        </Card.Body>
    </Card>
}

const TodaySchedule = ({ schedule, history }) => {
    const onClickBlockUnblock = (event) => {
        event.preventDefault()

        const action = schedule.blocked ? "unblock" : "block"

        axios
            .post(`http://localhost:5000/api/parking_lots/${schedule.parking_lot_id}/${action}`, {}, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            })
            .then((res) => {
                history.go(0)
            })
            .catch((e) => {
                alert(`Failed to block/unblock parking lot: ${e.response.data.error_message}`);
            });
    }


    return <Card
        bg={schedule.blocked ? "danger" : ""}
        text="nk"
        style={{ width: '18rem' }}
        className="mb-2"
    >
        <Card.Header>Today</Card.Header>
        <Card.Body>
            <Card.Title>Parking lot #{schedule.internal_id}</Card.Title>
            {!schedule.blocked &&
                <Button variant="warning" type="submit" className="company-approve" onClick={onClickBlockUnblock}>
                    Mark as blocked
                </Button>
            }
            {schedule.blocked &&
                <Card.Text>
                    This parking lot is blocked. Please find another one!
                </Card.Text>
            }
        </Card.Body>
    </Card>
}

const Schedules = ({ history }) => {
    const [schedules, setSchedules] = useState({ 'future_schedules': [], 'today_schedules': [] })

    const getSchedules = () => {
        axios
            .get('http://localhost:5000/api/parking_lot/books', {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            })
            .then((res) => {
                console.log(res.data)
                setSchedules(res.data)
            })
            .catch((e) => {
                alert(`Failed to fetch data: ${e.response.data.error_message}`);
            });
    }

    useEffect(() => {
        getSchedules()
    }, [])

    return <div className="schedules">
        {schedules.today_schedules.map((e, id) => {
            return <TodaySchedule key={id} schedule={e} history={history} />
        })}

        {schedules.future_schedules.map((e, id) => {
            return <FutureSchedule key={id} schedule={e} history={history} />
        })}
    </div>
}

const Employee = () => {
    const history = useHistory()

    return <div className="employee-view">
        <Schedules history={history} />
        <BookParkingLot history={history} />
    </div>
}

export default Employee