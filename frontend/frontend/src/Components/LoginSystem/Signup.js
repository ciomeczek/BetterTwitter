import Swal from 'sweetalert2';
import axios from 'axios'

function Signup(){
    (async () => {
  
    await Swal.fire({
      title: 'Zarejestruj się',
      html:
        '<input type="text" id="swal-input1"><br>' +
        '<input type="email" id="swal-input2"><br>' +
        '<input type="text" id="swal-input3"><br>' +
        '<input type="text" id="swal-input4"><br>' +
        '<input type="password" id="swal-input5"><br>',
      focusConfirm: false,
      preConfirm: () => {
        if(document.getElementById('swal-input1').value 
        && document.getElementById('swal-input2').value 
        && document.getElementById('swal-input3').value
        && document.getElementById('swal-input4').value
        && document.getElementById('swal-input5').value){
            return [
            document.getElementById('swal-input1').value,
            document.getElementById('swal-input2').value
            ]
        }
      }
    })
  
    if(document.getElementById('swal-input1').value 
        && document.getElementById('swal-input2').value 
        && document.getElementById('swal-input3').value
        && document.getElementById('swal-input4').value
        && document.getElementById('swal-input5').value) {
      //tutaj można dać axiosa z wysywałniem danych
      const username = document.getElementById('swal-input1').value;
      const email = document.getElementById('swal-input2').value;
      const first_name = document.getElementById('swal-input2').value;
      const last_name = document.getElementById('swal-input2').value;
      const password = document.getElementById('swal-input2').value;
      axios.post('localhost:8000/users/create', { username, email, first_name, last_name, password })
        //.then(()=>
        Swal.fire({
            toast: 'true',
            position: 'top-end',
            showConfirmButton: false,
            timer: 2000,
            timerProgressBar: true,
            icon: 'success',
            title: 'Zarejestrowany!'
        })//)
      //chyba coś takiego xD
    } else {
        Swal.fire({
            icon: 'error',
            title: 'Nie podałeś wszystkich danych'
        })
    }
  
    })()
  }
export default Signup;