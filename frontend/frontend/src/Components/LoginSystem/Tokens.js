import axios from 'axios'
// Od razu mówię że nie wiem czy takie "zwykłe" pliki .js są dozwolone w reactie więc jak coś to sobie to pozmieniasz

class TokenService {
    static async login(email, password) {
        return await axios.post('http://127.0.0.1:8000/token/', { username: email, password })
            .then((res) => {
                localStorage.setItem('access', res.data.access)
                localStorage.setItem('refresh', res.data.refresh)
                return true
            })
            .catch((err) => { return false })
    }

    static logout() {
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
    }

    static async refreshToken() {
        if (!localStorage.getItem('access'))
            // Przekieruj do strony z logowaniem
            return
        const token = localStorage.getItem('refresh')
        await axios.post('http://127.0.0.1:8000/token/refresh/', { refresh: token })
            .then((res) => {
                localStorage.setItem('access', res.data.access)
            })
            .catch((err) => {
                // przekieruj do strony z logowaniem
            })
    }

    static async getToken() {
        if (localStorage.getItem('access'))
            return await this.refreshToken()
                .then(() => {
                    return localStorage.getItem('access')
                })
        else { /*Przekieruj do strony z logowaniem*/ }
    }

    // W jaki sposób przesłać jwt (co zrobić jeśli musisz być zalogowany)
    /*
    const token = TokenService.getToken()
    axios.get(url, { headers: { Authorization: `Bearer ${token}` } })
    */

    static async register(username, password, first_name, last_name, email) {
        return await axios.post("http://127.0.0.1:8000/users/create/", {
            username,
            password,
            first_name,
            last_name,
            email
        })
            .then((res) => {
                if (res.status === 200) {
                    this.login(email, password)
                    // przekieruj gdzieś czy coś, w sumie jak chcesz xD
                    return null
                }
            })
            .catch((err) => {
                // Ważna rzecz, często będziesz miał errory typu unathorized, forbidden itd. Axios automatycznie gdy widzi że response ma kod inny niż 2xx robi errora. Później w dokumentacji opiszę kody errorów serwera (serwera w tym kontekście nie oznacza protokołu http)
                const errorCode = err.response.data.error_code
                if (errorCode.localeCompare('USERS-6'))
                    return 'taki email już istnieje'
                else if (errorCode.localeCompare('USERS-7'))
                    return 'taki username już istnieje'
            })
    }
}

export default TokenService
