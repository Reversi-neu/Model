import { Link, useNavigate } from "react-router-dom";
import "../../App.scss"
import "./sidebar.scss";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHouse, faUser, faBackward } from '@fortawesome/free-solid-svg-icons';
import { useToken } from "../../hooks/use_token";
import React from "react";

export function Sidebar() {
    const { token } = useToken();
    const [sidebar, setSidebar] = React.useState(false);
    const navigate = useNavigate();

    return (
        <div 
            className="icons" 
            style={{ zIndex: 10000 }} 
            onMouseLeave={() => {
                setTimeout(() => {
                    setSidebar(false);
                }, 300);
            }}
            onMouseEnter={() => {
                setSidebar(true);
            }}
        >
            <a style={{margin: '5px 5px 5px 0 '}}>
                <FontAwesomeIcon icon={faBackward} 
                    onClick={() => navigate(-1)}
                />
            </a>

            <Link to="/" className="icon">
                <FontAwesomeIcon icon={faHouse} />
            </Link>
            <div 
                className="sidebar"
                style={{
                    height: sidebar ? "100%" : "0",
                    width: sidebar ? "100%" : "0",
                    opacity: sidebar ? 1 : 0,
                }}
            >
                { token && 
                    <Link to="settings" className="icon">
                        <FontAwesomeIcon icon={faUser} />
                    </Link>
                }
            </div>
        </div>
    );
}