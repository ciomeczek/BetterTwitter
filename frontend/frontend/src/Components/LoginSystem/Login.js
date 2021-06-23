import Swal from 'sweetalert2';
import axios from 'axios'

function Login(){
    (async () => {
  
    await Swal.fire({
      title: 'Zaloguj się',
      html:
        '<input type="text" id="swal-input1" class="swal2-input" required>' +
        '<input type="password" id="swal-input2" class="swal2-input" required>',
      focusConfirm: false,
      preConfirm: () => {
        if(document.getElementById('swal-input1').value && document.getElementById('swal-input2').value){
            return [
            document.getElementById('swal-input1').value,
            document.getElementById('swal-input2').value
            ]
        }
      }
    })
  
    if (document.getElementById('swal-input1').value && document.getElementById('swal-input2').value) {
      //tutaj można dać axiosa z wysywałniem danych
      const username = document.getElementById('swal-input1').value;
      const password = document.getElementById('swal-input2').value;
      axios.post('localhost:8000/', { username, password })
        //.then(()=>
        Swal.fire({
            toast: 'true',
            position: 'top-end',
            showConfirmButton: false,
            timer: 2000,
            timerProgressBar: true,
            icon: 'success',
            title: 'Zalogowany!'
        })//)
      //chyba coś takiego
    } else {
        Swal.fire({
            icon: 'error',
            title: 'Nie podałeś wszystkich danych'
        })
    }
  
    })()
  }
export default Login;