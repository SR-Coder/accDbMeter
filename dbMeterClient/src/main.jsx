import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Root from './routes/Root.jsx';
import Debug from './routes/Debug.jsx';
import './index.css'

const router = createBrowserRouter([
  {
    path:"/",
    element: <Root />,
  },
  {
    path:"/debug",
    element:<Debug/>

  }
])


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
