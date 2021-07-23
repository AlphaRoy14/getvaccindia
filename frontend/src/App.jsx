import React, {useState} from 'react'
import { Typography, CssBaseline, Avatar, Button, TextField, FormControlLabel, Grid, Container, Checkbox, Link} from '@material-ui/core'
import { makeStyles } from '@material-ui/core/styles'



const useStyles = makeStyles((theme) => ({
  root: {
    minWidth: 275
  },
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: "5px",
  },
  avatar: {
    margin: theme.spacing(1),
    width: theme.spacing(15),
    height: theme.spacing(15),
  },
  form: {
    width: '100%', // IE 11 issue
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3,0,2)
  },
}))

const ThankingPage = () => {
  const classes = useStyles();
  return (

    <Container component="main" maxWidth="xs">
      <CssBaseline/>
      <div className={classes.paper}>
        <Typography component="body" variant="body1">
          Thanks for subscribing!
        </Typography>
      </div>
    </Container>
  )
}

const SignUp = () => {

  const axios = require("axios")

  const [SignUpView, setSignUpView]  = useState(false)

  const [email, setEamil] = useState("")
  const [name, setName] = useState("")
  const [zip, setZip] = useState("")
  const [doze1, setDoze1] = useState(true)
  const [doze2, setDoze2] = useState(false)

  const [emailError, setEmailError] = useState(false)
  const [zipError, setZipError] = useState(false)

  const handleEmail = (e) => setEamil(e.target.value)

  const handleName = (e) => setName(e.target.value)
  const handleZip = (e) => setZip(e.target.value)

  const handleDoze1 = e => setDoze1(e.target.checked)
  const handleDoze2 = e => setDoze2(e.target.checked)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (email === "") {
      setEmailError(true)
    }
    if (zip === "") {
      setZipError(true)
    }

    let dozes = []
    if (doze1) {
      dozes.push(1)
    }
    if (doze2) {
      dozes.push(2)
    }
    const obj = {
      "name": name,
      "email": email,
      "zip": zip,
      "dozes": dozes,
      "is_subscrived": true
    }
    console.log(email, name, zip, doze1, doze2, dozes, obj)

    if (email && zip && dozes.length) {
      axios.post("http://getvaccindia-env.eba-brene2w8.ap-south-1.elasticbeanstalk.com/api/v1/user/subscribe", obj)
        .then((response) => {
          console.log(response)
          setSignUpView(true)
        })
        .catch((error) => { console.log(error) })
    }
  }
  const classes = useStyles();
  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <Avatar className={classes.avatar} src="https://source.unsplash.com/EWKf48y_mx0" />
        <Typography component="h1" variant="h3">
          GetvaccIndia
        </Typography>
        <Typography component="h2" variant="caption">
          Sign up for email alerts!
        </Typography>
        <Typography component="h2" variant="caption">
          Get alerted whenever a new slot opens up in your area.
        </Typography>
        <form className={classes.Form} noValidate onSubmit={(e)=>handleSubmit(e)}>
          <TextField
            variant="outlined"
            margin="normal"
            required
            id="email"
            label="Email Address"
            name="email"
            autoComplete="email"
            type="email"
            fullWidth
            autoFocus
            onChange={(e) => handleEmail(e)}
            error={emailError}
          />
          <TextField
            variant="outlined"
            margin="normal"
            id="name"
            fullWidth
            label="whats your Name nigga?"
            name="full name"
            type="text"
            autoComplete="name"
            onChange={(e) => handleName(e)}
          />
          <TextField
            variant="outlined"
            margin="normal"
            id="zip"
            fullWidth
            label="Zip Code"
            name="zip"
            type="number"
            autoComplete="postal-code"
            required
            onChange={(e) => handleZip(e)}
            error={zipError}
          />
          <FormControlLabel
            control={<Checkbox value="doze 1" color="primary" onChange={(e)=>handleDoze1(e)} defaultChecked/>}
            label="Doze 1"
          />
          <FormControlLabel
            control={<Checkbox value="doze 2" color="primary" onChange={(e)=>handleDoze2(e)}/>}
            label="Doze 2"
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
          >
            Sign Up
          </Button>
          <Grid container>
            <Grid item sm>
              <Link href="https://apisetu.gov.in/public/marketplace/api/cowin" variant="body1">
                CoWin Public APIs
              </Link>
            </Grid>
          </Grid>

        </form>
        {SignUpView && <ThankingPage />}
      </div>
    </Container>
  )
};



const App = () => {
  return (
    <>
      <SignUp />
      {/* <CssBaseline />
      <Typography variant="h2" align="center" color="textPrimary" gutterBottom >GetvaccIndia</Typography> */}
    </>
  )
}

export default App