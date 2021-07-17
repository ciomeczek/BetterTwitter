import { useState } from 'react';
import axios from 'axios';

function Posts(){
    const [image, setImage] = useState();
    const [text, setText] = useState();
    let postArray = [];

    const handleImageChange = e => setImage(URL.createObjectURL(e.target.files[0]));
    const handleTextChange = e => setText(e.target);
    const handleSubmit = (e) => {
      e.preventDefault();
      axios.post('http://127.0.0.1:8000/create-post/', {text, image}).catch((err)=>{return false})
    }
        return (
          <div>
            <form onSubmit={handleSubmit}>
              <input type="file" onChange={handleImageChange} />
              <input type="text" onChange={handleTextChange} />
                <button>
                  Dodaj
                </button>
            </form>
          </div>
        );
      }
export default Posts;