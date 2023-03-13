import { Link } from "react-router-dom";
import "../App.scss"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHouse, faUser } from '@fortawesome/free-solid-svg-icons';
import { useToken } from "../hooks/use_token";

export function Icons() {
    const { token } = useToken();

    return (
        <div className="icons" style={{zIndex: 10000}}>
            <Link to="/" className="icon">
                <FontAwesomeIcon icon={faHouse} />
            </Link>
            { token && 
                <Link to="settings" className="icon">
                    <FontAwesomeIcon icon={faUser} />
                </Link>
            }
            
        </div>
    );
}