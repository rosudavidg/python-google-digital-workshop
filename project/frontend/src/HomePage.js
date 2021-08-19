import "./HomePage.css"
import { useHistory } from "react-router-dom";
import { Button } from 'react-bootstrap';

const HomePageLoginButton = ({ history }) => {
    const onClick = () => {
        history.push('/login')
    }

    return <Button variant="primary" type="submit" className="home-page-login-button" onClick={onClick}>
        Login
    </Button>
}

const HomePageRegisterButton = ({ history }) => {
    const onClick = () => {
        history.push('/register')
    }

    return <Button variant="success" type="submit" className="home-page-register-button" onClick={onClick}>
        Register
    </Button>
}


const Home = () => {
    const history = useHistory();

    return <div className="home-page">
        <HomePageLoginButton history={history} />
        <HomePageRegisterButton history={history} />
    </div>
}

export default Home