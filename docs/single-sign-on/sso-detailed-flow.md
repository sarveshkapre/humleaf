# How does OAuth OIDC Authentication Flow work in full stack web applications?


## Sequence Diagram

![mermaid-diagram-2023-05-19-173102](https://github.com/sarveshkapre/humleaf/assets/15698301/59d27adf-2fb9-4fa3-91af-be82635a6153)

## Steps

1.  User clicks on the Login button, initiating the OAuth 2.0 authentication process.
2.  The user is redirected to Google's authorization server (https://accounts.google.com/o/oauth2/v2/auth).
3.  The user logs into their Google account.
4.  The user consents to grant access.
5.  Google's authorization server redirects the user back to the client with an authorization code.
6.  The client receives the authorization code.
7.  The client sends the authorization code to the backend.
8.  The backend exchanges the authorization code for an access token and ID token at Google's token endpoint (https://oauth2.googleapis.com/token).
9.  The backend verifies the ID token.
10. The backend authenticates the user.
11. The backend sends the user's information to the frontend.
12. The frontend logs in the user.
13. The backend uses the access token to access Google APIs.
14. The backend uses the Refresh Token to obtain new access tokens when needed, by sending a request to Google's token endpoint (https://oauth2.googleapis.com/token).
15. The user clicks on the Logout button.
16. The backend ends the session and revokes the access token at Google's token revocation endpoint (https://oauth2.googleapis.com/revoke).
17. The backend sends a response to the frontend confirming the session has ended.
18. The frontend logs out the user.
19. The user is now logged out and can no longer access protected resources until they log in again.

## Deep Dive

Following is a deep dive into the OAuth OIDC Authentication Flow for a web application that uses Python/Flask as a backend and Next.js as a frontend.

1. **User clicks on the Login button (Next.js)**: The Next.js frontend constructs a URL to redirect the user to Google's authorization server. The URL includes query parameters such as the client ID, redirect URI, response type, scope, and state. The authorization server URL is `https://accounts.google.com/o/oauth2/v2/auth`.

2. **User is redirected to Google's authorization server (Next.js)**: The Next.js frontend redirects the user's browser to the constructed URL. This sends a GET request to Google's authorization server.

3. **User logs in to their Google account (Google)**: If the user is not already logged in to their Google account, they will be prompted to do so. This step involves Google's authentication server, not your web application.

4. **User consents to grant access (Google)**: After successful login, the user is presented with a consent screen. This screen shows what access the client is requesting (as specified by the scope). If the user agrees, they grant the client permission to access their data.

5. **Google's authorization server redirects the user back to the client (Google)**: After the user grants permission, Google's authorization server redirects the user back to the client's specified redirect URI. This redirect includes an authorization code in the URL query string.

6. **Client receives the authorization code (Next.js)**: The Next.js frontend receives the redirect from Google's authorization server. It extracts the authorization code from the URL query string.

7. **Client sends the authorization code to the backend (Next.js to Flask)**: The Next.js frontend sends a request to the Flask backend. This request includes the authorization code.

8. **Backend exchanges the authorization code for an access token and ID token (Flask)**: The Flask backend sends a POST request to Google's token endpoint (`https://oauth2.googleapis.com/token`). This request includes the authorization code, client ID, client secret, and redirect URI. Google's server verifies the code and credentials, and if valid, returns an access token and ID token.

9. **Backend verifies the ID token (Flask)**: The Flask backend decodes the ID token, which is a JSON Web Token (JWT). It verifies the signature, claims, and the issuer of the token. If the token is valid, the backend extracts the user's information from the token.

10. **Backend authenticates the user (Flask)**: The Flask backend uses the user's information from the ID token to authenticate the user. It may create a session or a session cookie, or issue a separate JWT, to maintain the user's authenticated state.

11. **Backend sends the user's information to the frontend (Flask to Next.js)**: The Flask backend sends a response to the Next.js frontend.

This response includes the user's information, and possibly a session cookie or JWT.

12. **Frontend logs in the user (Next.js)**: The Next.js frontend uses the user's information from the Flask backend to log in the user. It updates the user interface to reflect the user's authenticated state.

13. **Backend uses the access token to access Google APIs (Flask)**: If the Flask backend needs to access Google APIs on behalf of the user, it includes the access token in the Authorization header of its API requests.

14. **Using the Refresh Token (Flask)**: Access tokens have limited lifetimes. If your application needs access to a Google API beyond the lifetime of a single access token, it can obtain a refresh token. A refresh token allows your application to obtain new access tokens. This part of the flow handles what happens when an access token expires. The Flask backend sends a POST request to Google's token endpoint (`https://oauth2.googleapis.com/token`) with the refresh token, client ID, and client secret. If valid, Google's server returns a new access token (and optionally a new refresh token).

15. **User clicks on the Logout button (Next.js)**: When the user wants to end their session, they click on the Logout button. The Next.js frontend sends a request to the Flask backend to end the session.

16. **Backend ends the session (Flask)**: The Flask backend invalidates the user's session or session cookie, or the JWT it issued. It may also send a request to Google's token revocation endpoint (`https://oauth2.googleapis.com/revoke`) to revoke the access token, if it wants to ensure that the token can't be used anymore.

17. **Backend sends a response to the frontend (Flask to Next.js)**: The Flask backend sends a response to the Next.js frontend to confirm that the session has ended.

18. **Frontend logs out the user (Next.js)**: The Next.js frontend uses the response from the Flask backend to log out the user. It updates the user interface to reflect the user's unauthenticated state.

19. **User is logged out (Next.js)**: The user is now logged out and can no longer access protected resources until they log in again.

Please note that this is a high-level description of the OAuth OIDC flow using Google as the identity provider and Python/Flask and Next.js for the backend and frontend respectively. Actual implementations may vary based on specific requirements and environments. Always refer to the official documentation for the most accurate and up-to-date information.
