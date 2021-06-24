import React, { useState } from 'react';
import PostElement from "./PostElement";
import PostList from './PostList';

class Posts extends React.Component {
    constructor(props) {
        super(props);
        this.state = { items: [], title: '', text: '' };
        this.handleTextChange = this.handleTextChange.bind(this);
        this.handleTitleChange = this.handleTitleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
      }
    
      render() {
        return (
          <div>
            <h3>Dodaj post</h3>
            <PostElement items={this.state.items} />
            <form onSubmit={this.handleSubmit}>
              <input
                onChange={this.handleTitleChange}
                value={this.state.title}
              />
              <input
                onChange={this.handleTextChange}
                value={this.state.text}
              />
              <button>
                Dodaj
              </button>
            </form>
          </div>
        );
      }
    
      handleTextChange(e) {
        this.setState({ text: e.target.value });
      }
      handleTitleChange(e) {
        this.setState({ title: e.target.value });
      }
    
      handleSubmit(e) {
        e.preventDefault();
        if (this.state.text.length === 0) {
          return;
        }
        const newItem = {
          text: this.state.text,
          title: this.state.title,
          id: Date.now()
        };
        this.setState(state => ({
          items: state.items.concat(newItem),
          title: '',
          text: ''
        }));
      }
    }
export default Posts;