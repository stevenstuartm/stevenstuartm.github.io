---
layout: page
title: Resume
description: "Resume of Steven Stuart—software architect specializing in cloud-native solutions, AWS, .NET, and scalable system design."
permalink: /resume/
---

# Steven Stuart
**Software Architect**

<div class="social-icons">
  <a href="{{ site.social.github }}" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/>
    </svg>
  </a>
  <a href="{{ site.social.linkedin }}" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
    </svg>
  </a>
  <a href="mailto:{{ site.author.email }}" aria-label="Email" title="Email: {{ site.author.email }}">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
      <polyline points="22,6 12,13 2,6"></polyline>
    </svg>
  </a>
  <button class="copy-email-btn" data-email="{{ site.author.email }}" aria-label="Copy email address" title="Copy email address">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
    </svg>
  </button>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const copyBtn = document.querySelector('.copy-email-btn');
    if (copyBtn) {
        copyBtn.addEventListener('click', function() {
            const email = this.getAttribute('data-email');
            navigator.clipboard.writeText(email).then(() => {
                this.classList.add('copied');
                const originalTitle = this.getAttribute('title');
                this.setAttribute('title', 'Copied!');

                setTimeout(() => {
                    this.classList.remove('copied');
                    this.setAttribute('title', originalTitle);
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy email:', err);
            });
        });
    }
});
</script>

---


## Professional Summary

Passionate full-stack platform architect who loves building cloud-native solutions that scale and stand the test of time. Thrives on creating systems that not only perform beautifully and save costs, but also give teams the confidence that comes with rock-solid security and stability---all while keeping business goals front and center.

## Professional Experience

### System Architect | True Market Insiders -- St. Petersburg, FL | Feb 2023 -- Present

Spearheaded the modernization of IT operations for a financial research firm. Directed cloud infrastructure strategy, mentored developers, and advised leadership on architecture, security, and deployment. Delivered secure, highly available cloud solutions and implemented enterprise-grade development pipelines.

- Cut IT overhead by 80% by refactoring cloud infrastructure and streamlining services.
- Strengthened security with compliant APIs, AWS WAF integration, and zero-trust IAM policies.
- Increased performance and data resilience by rearchitecting storage and data platforms.
- Built CI/CD pipelines and dedicated testing environments, improving deployment quality.

*Technologies: .NET 8, ASP.NET, AWS EKS, GraphQL (HotChocolate), AWS Aurora RDS, DynamoDB, Snowflake, CloudWatch, S3, EventBridge, CloudFront, WAF, IAM, VPN, CodeBuild, Vue.js, .NET MAUI*

### Senior Software Engineer II | Alkami Technology -- Plano, TX | Jul 2018 -- Jan 2023

Developed scalable microservices and event-driven systems for a leading digital banking platform. Collaborated across Agile teams to enhance delivery velocity and product stability. Provided mentorship through code reviews and best-practice enforcement.

- Developed Alkami's first AWS serverless APIs, boosting scalability and development velocity..
- Created real-time notification platform adopted across client banks.
- Led code reviews and mentored junior developers on clean code principles.

*Technologies: .NET, ASP.NET, AWS Lambda, SQS, DynamoDB, SQL Server, Vue.js*

### Solutions Developer III | Cottonwood Financial -- Irving, TX | Feb 2015 -- Jun 2018

Contributed to enterprise application development for financial services. Led initiatives to modernize legacy codebases, improve system modularity, and integrate robust testing.

- Built WPF-based point-of-sale system used at hundreds of retail locations.
- Refactored monolithic services into a modular architecture, improving scalability.
- Developed test automation tools that reduced QA cycle time and accelerated defect detection.

*Technologies: .NET, ASP.NET, WCF, SQL Server, WPF, MongoDB*

### Tech Lead | DealerSpeedLeads -- Dallas, TX | Mar 2011 -- Feb 2015

Led the full-stack development of scalable SaaS products and automation tools for a growing marketing technology company. Balanced client engagement, system architecture, and internal tooling development.

- Designed a scalable, configurable inventory platform supporting multiple industries.
- Developed distributed automation services executing thousands of daily operations.
- Delivered internal tools, deployment pipelines, and customer-facing web apps.

*Technologies: .NET, ASP.NET, MySQL, WPF, WinForms, Selenium*

## Education

**B.S., Computer Information Systems**

DeVry University -- Irving, TX | Oct 2008 -- Jun 2012

## Keywords & Skills

.NET • ASP.NET • AWS (EKS, Lambda, WAF, Aurora, SQS) • GraphQL • Vue.js • CI/CD • Security Architecture • SQL Server • DynamoDB • Event-Driven Architecture • Microservices • Cloud Architecture • DevOps • WPF • Agile • System Design • Software Mentorship