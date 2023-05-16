import React from "react";
import { Link } from "react-router-dom";
import "./NavBar.scss"
import VicLogo from "../../static/figure/VicGov.png"
import AusLogo from "../../static/figure/aus.png"

const NavBar = () => {
	return (
		<div className="navbar">
      <div className="logo">
					<img src={VicLogo} alt="VicLogo"/>
          <span>
            Victorians' Happiness {String.fromCodePoint(0x1F603)}{String.fromCodePoint(0x1F61E)}
          </span>
			</div>

      <div className="links">
        <Link className="link" to="/">
          <h3>Home</h3>
        </Link>
        <Link className="link" to="/map">
          <h3>Map</h3>
        </Link>
        {/* <Link className="link" to="/aboutme">
          <h3>About me</h3>
        </Link>
        <Link className="link" to="/blogs">
          <h3>Blogs</h3>
        </Link>
        <Link className="link" to="#">
          <h3>Feedback</h3>
        </Link> */}
        
        <img src={AusLogo} alt="AusLogo"/>
        {/* <span>{curUser}</span>
        {loginState ? 
          <span>logout</span> : <span>login</span>
        }

        {!loginState && <SvgIcon component={AccountCircleIcon}/>} */}
        
        {/* <span className="write">
          <Link classname="link" to="/write">Write</Link>
        </span> */}

      </div>
			
			

			
    </div>
	)
}

// const NavBar = () => {
// 	return (
// 		<div className="navbar">
// 			<div className="container">
// 				<div className="logo">
// 					<img src={Logo}/>
// 				</div>
// 				<div className="links">
// 					<Link className="link" to="/?cat=art">
// 						<h6>ART</h6>
// 					</Link>
// 					<Link className="link" to="/?cat=science">
// 						<h6>SCIENCE</h6>
// 					</Link>
// 					<Link className="link" to="/?cat=technology">
// 						<h6>TECHNOLOGY</h6>
// 					</Link>
// 					<Link className="link" to="/?cat=cinema">
// 						<h6>CINEMA</h6>
// 					</Link>
// 					<Link className="link" to="/?cat=design">
// 						<h6>DESIGN</h6>
// 					</Link>
// 					<Link className="link" to="/?cat=food">
// 						<h6>FOOD</h6>
// 					</Link>
// 					<span>John</span>
// 					<span>Logout</span>
// 					<span className="write">
// 						<Link classname="link" to="/write">Write</Link>
// 					</span>
// 				</div>
// 			</div>
// 		</div>
// 	)
// }

export default NavBar