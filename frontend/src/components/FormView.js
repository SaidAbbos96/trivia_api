import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/FormView.css';

class FormView extends Component {
  constructor(props){
    super();
    this.state = {
      question: "",
      answer: "",
      difficulty: 1,
      category: 1,
      categories: [],
    }
  }

  componentDidMount(){
    $.ajax({
      url: `/categories`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories })
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
        return;
      }
    })
  }


  submitQuestion = (event) => {
    event.preventDefault();
    $.ajax({
      url: '/questions', //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        category: this.state.category
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById("add-question-form").reset();
        return;
      },
      error: (error) => {
        alert('Unable to add question. Please try your request again')
        return;
      }
    })
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }
  render() {
    return (
      <div id="add-form">
        <h2>Add a New Trivia Question</h2>
        <form className="form-view" id="add-question-form" onSubmit={this.submitQuestion}>
          <label>Question<span class="reqstar"> *</span></label>
            <input type="text" name="question" onChange={this.handleChange}/>
          <label>Answer<span class="reqstar"> *</span></label>
            <input type="text" name="answer" onChange={this.handleChange}/>
          
          <label>Difficulty<span class="reqstar"> *</span></label>
            <select name="difficulty" onChange={this.handleChange}>
              <option value="1">★</option>
              <option value="2">★★</option>
              <option value="3">★★★</option>
              <option value="4">★★★★</option>
              <option value="5">★★★★★</option>
            </select>
          
          <label>Category<span class="reqstar"> *</span></label>
            <select name="category" onChange={this.handleChange}>
              {this.state.categories.map((category) => {
                  return (
                    <option key={category.id} value={category.id}>{category.type}</option>
                  )
                })}
            </select>
          
          <input type="submit" className="button add-button" value="Submit" />
        </form>
      </div>
    );
  }
}

export default FormView;