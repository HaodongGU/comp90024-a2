import React, { useEffect }from "react";
import { Link } from "react-router-dom";
import Fade from 'react-reveal/Fade';
import Swing from 'react-reveal/Swing';
import SadEmoji from "../../static/figure/sadEmoji.png"
import HappyEmoji from "../../static/figure/happyEmoji.png"
import axios from "axios";
import "./Home.scss"

const ip = process.env.REACT_APP_IP;
console.log("home env ip: ", process.env.REACT_APP_IP);

class FadeExample extends React.Component {
  render() {
    return (
      // <div >
      //   <Swing down>
      //     <div className="title_home">
      //       <h1 className="greeting_w">What Correlates with Victorians' Happiness?</h1>
      //     </div>
      //   </Swing>
      // </div>

      <div className="home_main">
        {/* <Fade left>
        <img src={HappyEmoji}/>
        </Fade> */}

        <Swing down>
          <h1 className="greeting_w">What Correlates with Victorians' Sentiments?</h1>
        </Swing>

        {/* <Fade right>
        <img src={SadEmoji}/>
        </Fade> */}
      </div>
    );
  }
}

const Home = () => {
  useEffect(() => {
    const testConnections = async () => {
      try {
        const url = "http://"+ip+":5000/hello_world_json";
        const res0 = await axios.get(url);
        console.log("res0: ", res0);
        console.log("res0 data: ", res0.data);
      } catch (err) {
        console.log(err);
      }
    };
    testConnections();
  }, []);

  return (
    <div>
      <FadeExample/>
    </div>
  )
}

export default Home