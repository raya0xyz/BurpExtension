# Burp Suite Extension Development - Jython Practice & Research

This repository contains my practice and research on developing extensions for Burp Suite using Jython (Python 2.7 syntax). The goal is to understand how to extend Burp Suite functionality for security testing, request logging, and advanced techniques like cache poisoning DoS.

## Repository Structure

| File         | Description |
|--------------|-------------|
| `A01xt.py`   | A simple demo extension that attaches to Burp and prints a message in the console. Great for learning the basics of Burp extension development. |
| `A02xt.py`   | A basic HTTP request logger that logs all requests coming through the proxy and extracts the HTTP method and URL. |
| `cache-poison.py`   | An advanced extension that performs Long Header Cache Poisoning DoS. Right-click a request in Burp, go to Extensions, and select this extension to send a modified request with an oversized header to trigger a denial-of-service condition. |

## Requirements

- Burp Suite Professional
- Jython standalone (2.7.x recommended)
- Basic knowledge of Python and Java interoperability via Jython

## How to Use

### For All Extensions:
1. Open Burp Suite > Extender > Extensions > Add
2. Select Python as the extension type
3. Browse and load the `.py` file you want to use

---

### cache.py: Long Header Cache Poisoning DoS
#### Steps:
1. Intercept or browse to any HTTP request in Burp.
2. Right-click the request in the context menu.
3. Go to Extensions > [cache].
4. The extension will automatically modify the request by adding a large custom header (`X-Cache-Poison`) and resend it.

**Note**: This technique may cause memory exhaustion or timeouts on vulnerable servers. Use responsibly and only in authorized environments.

---

## Learning Resources

- [Burp Suite Extender Documentation](https://portswigger.net/burp/extensibility)
- [Jython Essentials](https://jython.readthedocs.io/en/latest/)
- OWASP Cheat Sheets on Cache Poisoning and Advanced Web Attacks

---

## Contributions

Feel free to fork, contribute, or report issues if you'd like to improve any of the extensions or add new ones.

---

## License

MIT License — See [LICENSE](LICENSE) for more details.

--- 
