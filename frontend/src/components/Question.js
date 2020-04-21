import React, { Component } from 'react';
import '../stylesheets/Question.css';

class Question extends Component {
  constructor(){
    super();
    this.state = {
      visibleAnswer: false
    }
  }

  flipVisibility() {
    this.setState({visibleAnswer: !this.state.visibleAnswer});
  }

  render() {
    const { question, answer, category, difficulty } = this.props;
    return (
      <div className="Question-holder">
        <div className="Question"><img className="category" alt="thisimage" src={`${category.type.toLowerCase()}.svg`}/>  {question}</div>
        <div className="Question-status">
          
        <div className="difficulty">Difficulty: {'🏆'.repeat(difficulty)}</div>
        <div class="delete-div" onClick={() => this.props.questionAction('DELETE')}>
       <img src="delete.png" className="delete" alt="thisimage"/>
          Delete the Quession
          </div>
        </div>
        <div className="show-answer button"
            onClick={() => this.flipVisibility()}> 
            {this.state.visibleAnswer ? 'Hide' : 'Show'} Answer
          </div>
        <div className="answer-holder">
          <span style={{"visibility": this.state.visibleAnswer ? 'visible' : 'hidden'}}>Answer: {answer}</span>
        </div>
      </div>
    );
  }
}

export default Question;
