import React from "react";
import { Link } from "react-router-dom";
import Fade from 'react-reveal/Fade';
import Swing from 'react-reveal/Swing';
import SadEmoji from "../../static/figure/sadEmoji.png"
import HappyEmoji from "../../static/figure/happyEmoji.png"

import "./Home.scss"

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
  return (
    <div>
      <FadeExample/>
    </div>
  )
}

export default Home