(() => {
  const form = document.getElementById("donateForm");
  if (!form) return;

  const amountInput = document.getElementById("donateAmount");
  const causeSelect = document.getElementById("causeSelect");
  const statusEl = document.getElementById("donateStatus");
  const submitBtn = document.getElementById("donateSubmit");
  const minAmount = Number(form.dataset.min || 100);

  const showStatus = (message, kind) => {
    if (!statusEl) return;
    statusEl.hidden = !message;
    statusEl.textContent = message || "";
    statusEl.className = "donate-status" + (kind ? " donate-status--" + kind : "");
  };

  document.querySelectorAll(".amount-chips button").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (amountInput) amountInput.value = btn.dataset.amount;
      document.querySelectorAll(".amount-chips button").forEach((b) => b.classList.remove("is-active"));
      btn.classList.add("is-active");
    });
  });

  document.querySelectorAll(".js-select-cause").forEach((link) => {
    link.addEventListener("click", () => {
      if (causeSelect) causeSelect.value = link.dataset.cause;
    });
  });

  const csrfToken = () => {
    const input = form.querySelector("[name=csrfmiddlewaretoken]");
    return input ? input.value : "";
  };

  const selectedPaymentMethod = () => {
    const checked = form.querySelector("input[name=payment_method]:checked");
    return checked ? checked.value : "upi";
  };

  const selectedDonationType = () => {
    const checked = form.querySelector("input[name=donation_type]:checked");
    return checked ? checked.value : "one-time";
  };

  const razorpayMethodConfig = (method) => {
    // Prefer the donor's selected method in Razorpay Checkout display
    const blocks = {
      upi: {
        name: "Pay using UPI",
        instruments: [{ method: "upi" }],
      },
      google_pay: {
        name: "Pay using Google Pay",
        instruments: [{ method: "upi", apps: ["google_pay"] }],
      },
      phonepe: {
        name: "Pay using PhonePe",
        instruments: [{ method: "upi", apps: ["phonepe"] }],
      },
      card: {
        name: "Pay using Card",
        instruments: [{ method: "card" }],
      },
      netbanking: {
        name: "Pay using Net Banking",
        instruments: [{ method: "netbanking" }],
      },
    };
    const key = blocks[method] ? method : "upi";
    return {
      display: {
        blocks: {
          preferred: blocks[key],
        },
        sequence: ["block.preferred"],
        preferences: {
          show_default_blocks: true,
        },
      },
    };
  };

  const payloadFromForm = () => ({
    donation_type: selectedDonationType(),
    cause: form.cause.value,
    amount: Number(form.amount.value),
    name: form.name.value.trim(),
    email: form.email.value.trim(),
    phone: (form.phone.value || "").trim(),
    pan: (form.pan.value || "").trim().toUpperCase(),
    updates: form.updates.checked,
    payment_method: selectedPaymentMethod(),
  });

  const openCheckout = (data, paymentMethod) => {
    if (typeof Razorpay === "undefined") {
      showStatus("Razorpay checkout could not load. Please refresh and try again.", "error");
      return;
    }
    const options = {
      key: data.key_id,
      amount: data.amount,
      currency: data.currency || "INR",
      name: data.name || "Vaaradhi Trust",
      description: data.description || "Donation",
      image: "/static/img/logo.svg",
      prefill: data.prefill || {},
      notes: {
        ...(data.notes || {}),
        payment_method: paymentMethod,
      },
      theme: data.theme || { color: "#c45c26" },
      config: razorpayMethodConfig(paymentMethod),
      handler: async (response) => {
        try {
          const verifyRes = await fetch(form.dataset.verifyUrl, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken(),
            },
            body: JSON.stringify({
              donation_id: data.donation_id,
              razorpay_order_id: response.razorpay_order_id || data.order_id || "",
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature,
              razorpay_subscription_id:
                response.razorpay_subscription_id || data.subscription_id || "",
            }),
          });
          const verifyData = await verifyRes.json();
          if (!verifyRes.ok) {
            throw new Error(verifyData.detail || "Could not verify payment.");
          }
          window.location.href = verifyData.redirect || "/donate/thank-you/";
        } catch (err) {
          showStatus(
            err.message || "Payment received but verification failed. Please contact us.",
            "error"
          );
          window.location.href = "/donate/failed/";
        }
      },
      modal: {
        ondismiss: () => {
          showStatus("Checkout closed. You can try again whenever you are ready.", "info");
          if (submitBtn) submitBtn.disabled = false;
        },
      },
    };
    if (data.subscription_id) {
      options.subscription_id = data.subscription_id;
    } else {
      options.order_id = data.order_id;
    }
    const rzp = new Razorpay(options);
    rzp.on("payment.failed", () => {
      showStatus("Payment was not completed. Please try again.", "error");
      if (submitBtn) submitBtn.disabled = false;
    });
    rzp.open();
  };

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = payloadFromForm();
    if (!payload.cause) {
      showStatus("Please choose a cause.", "error");
      return;
    }
    if (!payload.amount || payload.amount < minAmount) {
      showStatus("Minimum online donation is ₹" + minAmount + ".", "error");
      return;
    }
    if (!payload.payment_method) {
      showStatus("Please select a payment method.", "error");
      return;
    }
    if (submitBtn) submitBtn.disabled = true;
    showStatus("Connecting to secure checkout…", "info");

    try {
      const res = await fetch(form.dataset.orderUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken(),
        },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (res.status === 503 || data.configured === false) {
        showStatus(
          data.detail ||
            "Razorpay keys are not added yet. Add RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET in .env, then restart the server.",
          "info"
        );
        if (submitBtn) submitBtn.disabled = false;
        return;
      }
      if (!res.ok) {
        const detail =
          data.detail ||
          (data.amount && data.amount[0]) ||
          (data.cause && data.cause[0]) ||
          "Could not start donation. Please check the form and try again.";
        throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
      }
      openCheckout(data, payload.payment_method);
    } catch (err) {
      showStatus(err.message || "Something went wrong. Please try again.", "error");
      if (submitBtn) submitBtn.disabled = false;
    }
  });
})();
