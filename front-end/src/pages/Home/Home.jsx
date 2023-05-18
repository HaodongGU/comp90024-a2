import React, { useEffect }from "react";
import { Link } from "react-router-dom";
import Fade from 'react-reveal/Fade';
import Swing from 'react-reveal/Swing';
import SadEmoji from "../../static/figure/sadEmoji.png"
import HappyEmoji from "../../static/figure/happyEmoji.png"
import axios from "axios";
import "./Home.scss"

const ip="localhost";

class FadeExample extends React.Component {
  render() {
    return (
      <div className="home_main">
        <Fade left>
        <img src={HappyEmoji}/>
        </Fade>

        <Swing down>
          <div className="title_home">
            {/* <h1 className="greeting_r">What </h1>
            <h1 className="greeting_g">Correlates with </h1>
            <h1 className="greeting_b">Victorians' Happiness? </h1> */}
            <h1 className="greeting_w">What Correlates with Victorians' Happiness?</h1>
          </div>
        </Swing>

        <Fade right>
        <img src={SadEmoji}/>
        </Fade>
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