//This script is used to generate the temporary token used for authorizing the app for accessing the user data



var request = require('request'); // "Request" library

function getSpotifyUserData(client_id, client_secret, callback) {
  // Your application requests authorization
  var authOptions = {
    url: 'https://accounts.spotify.com/api/token',
    headers: {
      'Authorization': 'Basic ' + (new Buffer.from(client_id + ':' + client_secret).toString('base64'))
    },
    form: {
      grant_type: 'client_credentials'
    },
    json: true
  };

  request.post(authOptions, function(error, response, body) {
    if (!error && response.statusCode === 200) {
      // Use the access token to access the Spotify Web API
      var token = body.access_token;
      console.log(token)
    } else {
      callback(error, null);
    }
  });
}

// Replace 'CLIENT_ID' and 'CLIENT_SECRET' with your actual credentials
var client_id = 'Your app client id';
var client_secret = 'Your app client secret';

// Call the function and handle the response
getSpotifyUserData(client_id, client_secret, function(error, userData) {
  if (error) {
    console.error('Error:', error);
  } else {
    console.log('User Data:', userData);
  }
});
