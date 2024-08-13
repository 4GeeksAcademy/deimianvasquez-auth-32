import React, { useState, useContext } from "react"
import { Context } from "../store/appContext"
import { useSearchParams } from "react-router-dom"

const UpdatePassword = () => {

    const { actions } = useContext(Context)

    const [newPass, setNewPass] = useState("")

    const [searchParams, _] = useSearchParams();



    const handleSubmit = async (event) => {
        event.preventDefault()

        const response = actions.updatePassword(searchParams.get("token"), newPass)
        console.log(response)
    }


    return (
        <div className="container">
            <div className="row justify-content-center">
                <h2 className="text-center my-3"> Actualizar contraseña:)</h2>
                <div className="col-12 col-md-6 border py-4">
                    <form
                        onSubmit={handleSubmit}
                    >
                        <div className="form-group mb-3">
                            <label htmlFor="btnEmail">Correo:</label>
                            <input
                                type="text"
                                placeholder="new password"
                                className="form-control"
                                id="btnEmail"
                                name="password"
                                value={newPass}
                                onChange={(event) => setNewPass(event.target.value)}
                            />
                        </div>

                        <button className="btn btn-outline-primary w-100">Enviar</button>
                    </form>
                </div>

                <div className="w-100"></div>

                {/* <br/> */}
            </div>
        </div>
    )
}

export default UpdatePassword