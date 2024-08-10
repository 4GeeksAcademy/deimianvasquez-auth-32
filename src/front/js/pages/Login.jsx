import React, { useState, useContext } from "react"
import { Link } from "react-router-dom"
import { Context } from "../store/appContext"

const initialState = {
    email: "",
    password: ""
}

const Login = () => {
    const { actions } = useContext(Context)

    const [user, setUser] = useState(initialState)

    const handleChange = (event) => {
        setUser({
            ...user,
            [event.target.name]: event.target.value
        })
    }

    const handleSubmit = async (event) => {
        event.preventDefault()
        try {
            const response = await actions.login(user)
            console.log(response)
        } catch (error) {
            console.log(error)
        }


    }


    return (
        <div className="container">
            <div className="row justify-content-center">
                <h2 className="text-center my-3">Ingresa en nuestra plataforma :)</h2>
                <div className="col-12 col-md-6 border py-4">
                    <form 
                        onSubmit={handleSubmit}
                    >
                        <div className="form-group mb-3">
                            <label htmlFor="btnEmail">Correo:</label>
                            <input
                                type="text"
                                placeholder="elmero@gmail.com"
                                className="form-control"
                                id="btnEmail"
                                name="email"
                                value={user.email}
                                onChange={handleChange}
                            />
                        </div>

                        <div className="form-group mb-3">
                            <label htmlFor="btnPassword">Contraseña:</label>
                            <input
                                type="password"
                                placeholder="elmero@gmail.com"
                                className="form-control"
                                id="btnPassword"
                                name="password"
                                value={user.password}
                                onChange={handleChange}
                            />
                        </div>
                        <button className="btn btn-outline-primary w-100">Inicia sesión</button>
                    </form>
                </div>

                <div className="w-100"></div>

                {/* <br/> */}

                <div className="col-12 col-md-6 d-flex justify-content-between my-1">
                    <Link to={"/register"}>Registrarme</Link>
                    <Link to={"/recovery-password"}>Olvido su contraseña</Link>
                </div>
            </div>
        </div>
    )
}


export default Login