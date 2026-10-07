import json
import asyncio
import random
import os
from playwright.async_api import async_playwright

FORM_URL = "https://docs.google.com/forms/d/1imljc_2-ooJ5fon4IMUraDVC4uP-F7IamOD2_UrbbSc/viewform"

MIN_DELAY = 2 * 60
MAX_DELAY = 5 * 60

async def question_block(page, question):
    block = page.locator("div[role='listitem']").filter(has_text=question).first
    if await block.count() == 0:
        block = page.locator("div[jsname='WsjYwc']").filter(has_text=question).first
    if await block.count() == 0:
        raise Exception(f"Pertanyaan tidak ditemukan: {question}")
    return block

async def fill_text(page, question, value):
    block = await question_block(page, question)
    inp = block.locator("input[type='text']").first
    if await inp.count():
        await inp.fill(str(value))
        return
    ta = block.locator("textarea").first
    if await ta.count():
        await ta.fill(str(value))
        return
    raise Exception(f"Field teks tidak ditemukan: {question}")

async def choose(page, question, value):
    block = await question_block(page, question)

    dropdown = block.locator("[role='listbox']").first
    if await dropdown.count():
        await dropdown.click()
        option = page.locator("[role='option']").filter(has_text=str(value)).first
        if await option.count() == 0:
            raise Exception(f"Pilihan '{value}' tidak ditemukan pada {question}")
        await option.click()
        return

    option = block.get_by_text(str(value), exact=True).first
    if await option.count():
        await option.click()
        return

    raise Exception(f"Pilihan '{value}' tidak ditemukan pada {question}")

async def submit_form(page):
    # Google Forms biasanya memakai tombol role=button bernama Submit/Kirim.
    for name in ["Submit", "Kirim"]:
        button = page.get_by_role("button", name=name, exact=True)
        if await button.count():
            await button.click()
            return

    # Fallback selector Google Forms.
    button = page.locator("[jsname='M2vV3'][role='button']").first
    if await button.count():
        await button.click()
        return

    raise Exception("Tombol Submit/Kirim tidak ditemukan.")

async def main():
    with open("data.json", encoding="utf-8") as f:
        students = json.load(f)

    print(f"Total data: {len(students)}")

    async with async_playwright() as p:
        # Lokal: browser terlihat. GitHub Actions: gunakan headless.
        headless = os.getenv("CI", "").lower() == "true"
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(FORM_URL, wait_until="domcontentloaded")
        await page.wait_for_timeout(1500)

        # Pada GitHub Actions, form harus dapat diakses tanpa login.
        # Jangan memasukkan password Google ke repository/secrets.
        if "accounts.google.com" in page.url:
            raise RuntimeError(
                "Form meminta login Google. GitHub Actions tidak dapat login "
                "menggunakan password yang ditanam di script. Gunakan form "
                "yang dapat diisi tanpa login atau jalankan secara lokal."
            )

        for i, s in enumerate(students, 1):
            if i > 1:
                await page.goto(FORM_URL, wait_until="domcontentloaded")
                await page.wait_for_timeout(1200)

            print(
                f"[{i}/{len(students)}] {s['nama']} | "
                f"{s['nim']} | {s['program_studi']} | {s['angkatan']}"
            )

            await fill_text(page, "Nama Lengkap", s["nama"])
            await fill_text(page, "NIM", s["nim"])
            await choose(page, "Program Studi", s["program_studi"])
            await choose(page, "Angkatan", s["angkatan"])

            await submit_form(page)
            print("  ✓ Submitted")

            if i < len(students):
                delay = random.randint(MIN_DELAY, MAX_DELAY)
                print(f"  Menunggu {delay//60} menit {delay%60} detik...")
                await asyncio.sleep(delay)

        await browser.close()
        print("Semua data selesai disubmit.")

if __name__ == "__main__":
    asyncio.run(main())
